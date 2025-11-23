"""
Web server for Pick-a-Page story tool.

Provides a child-friendly web interface for browsing, creating, and playing stories.
Uses only Python stdlib (http.server, no external dependencies).
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from pathlib import Path
from typing import Dict, List, Any
import mimetypes

from .compiler import StoryCompiler, ValidationError, Story
from .generator import HTMLGenerator


def is_safe_path(base_dir: Path, requested_path: str) -> tuple[bool, Path]:
    """
    Validate that requested_path is safe and within base_dir.
    Returns (is_safe, resolved_path).
    """
    try:
        # Remove any directory traversal attempts
        if '..' in requested_path or requested_path.startswith('/'):
            return False, Path()
        
        # Ensure only filename (no path separators except for expected format)
        if '/' in requested_path or '\\' in requested_path:
            # Allow only simple paths like "story.txt", not "../story.txt"
            parts = requested_path.split('/')
            if any('..' in part or part.startswith('.') for part in parts):
                return False, Path()
        
        # Resolve full path
        full_path = (base_dir / requested_path).resolve()
        
        # Ensure the resolved path is still within base_dir
        if not str(full_path).startswith(str(base_dir.resolve())):
            return False, Path()
        
        return True, full_path
    except (ValueError, OSError):
        return False, Path()


class StoryHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for the story server."""
    
    def __init__(self, *args, stories_dir: Path, output_dir: Path, **kwargs):
        self.stories_dir = stories_dir
        self.output_dir = output_dir
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_index()
        elif parsed_path.path == '/api/stories':
            self.serve_story_list()
        elif parsed_path.path.startswith('/api/story/'):
            story_name = parsed_path.path.split('/')[-1]
            self.serve_story_content(story_name)
        elif parsed_path.path.startswith('/play/'):
            story_name = parsed_path.path.split('/')[-1].replace('.html', '')
            self.serve_compiled_story(story_name)
        elif parsed_path.path.startswith('/output/'):
            # Serve compiled HTML files
            self.serve_output_file(parsed_path.path)
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/compile':
            self.compile_story()
        elif parsed_path.path == '/api/validate':
            self.validate_story()
        elif parsed_path.path == '/api/save':
            self.save_story()
        else:
            self.send_error(404, "Endpoint not found")
    
    def serve_index(self):
        """Serve the main HTML interface."""
        html = get_index_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        # Security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Content-Security-Policy', "default-src 'self' 'unsafe-inline' 'unsafe-eval'")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_story_list(self):
        """Serve JSON list of available stories."""
        stories = []
        
        # Scan stories directory for .txt files
        if self.stories_dir.exists():
            for story_file in self.stories_dir.glob('*.txt'):
                try:
                    # Read first few lines to get metadata
                    with open(story_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Try to parse to get title/author
                    compiler = StoryCompiler()
                    story = compiler.parse(content)
                    stories.append({
                        'filename': story_file.name,
                        'title': story.metadata.title,
                        'author': story.metadata.author,
                        'sections': len(story.sections)
                    })
                except Exception as e:
                    # If parsing fails, just use filename
                    stories.append({
                        'filename': story_file.name,
                        'title': story_file.stem.replace('_', ' ').title(),
                        'author': 'Unknown',
                        'error': str(e)
                    })
        
        self.send_json_response(stories)
    
    def serve_story_content(self, story_name: str):
        """Serve the raw content of a story file."""
        # Validate path safety
        is_safe, story_path = is_safe_path(self.stories_dir, story_name)
        if not is_safe:
            self.send_error(403, "Invalid file path")
            return
        
        if not story_path.exists() or not story_path.is_file():
            self.send_error(404, f"Story not found: {story_name}")
            return
        
        try:
            with open(story_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_json_response({'content': content, 'filename': story_name})
        except Exception as e:
            self.send_error(500, f"Error reading story: {str(e)}")
    
    def serve_compiled_story(self, story_name: str):
        """Serve a compiled HTML story."""
        # Validate path safety
        is_safe, html_path = is_safe_path(self.output_dir, f"{story_name}.html")
        if not is_safe:
            self.send_error(403, "Invalid file path")
            return
        
        if not html_path.exists():
            self.send_error(404, f"Compiled story not found: {story_name}")
            return
        
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error serving story: {str(e)}")
    
    def serve_output_file(self, path: str):
        """Serve files from output directory."""
        # Extract just the filename from the path
        filename = path.replace('/output/', '').lstrip('/')
        
        # Validate path safety
        is_safe, file_path = is_safe_path(self.output_dir, filename)
        if not is_safe:
            self.send_error(403, "Invalid file path")
            return
        
        if not file_path.exists() or not file_path.is_file():
            self.send_error(404, "File not found")
            return
        
        # Guess mime type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error serving file: {str(e)}")
    
    def compile_story(self):
        """Compile a story from POST data."""
        content_length = int(self.headers['Content-Length'])
        
        # Limit request size to prevent DOS (10MB max)
        MAX_REQUEST_SIZE = 10 * 1024 * 1024
        if content_length > MAX_REQUEST_SIZE:
            self.send_error(413, "Request entity too large")
            return
        
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            story_content = data.get('content', '')
            story_name = data.get('filename', 'story.txt').replace('.txt', '')
            
            # Sanitize filename - allow only alphanumeric, dash, underscore
            import re
            story_name = re.sub(r'[^a-zA-Z0-9_-]', '_', story_name)
            if not story_name:
                story_name = 'story'
            
            # Parse and validate
            compiler = StoryCompiler()
            story = compiler.parse(story_content)
            errors = compiler.validate(story)
            
            if errors:
                self.send_json_response({
                    'success': False,
                    'errors': errors
                }, status=400)
                return
            
            # Generate HTML
            generator = HTMLGenerator()
            html_content = generator.generate(story, base_path=Path.cwd())
            
            # Save to output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)
            html_path = self.output_dir / f"{story_name}.html"
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.send_json_response({
                'success': True,
                'message': 'Story compiled successfully',
                'play_url': f'/play/{story_name}'
            })
        
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    def validate_story(self):
        """Validate a story from POST data."""
        content_length = int(self.headers['Content-Length'])
        
        # Limit request size to prevent DOS (10MB max)
        MAX_REQUEST_SIZE = 10 * 1024 * 1024
        if content_length > MAX_REQUEST_SIZE:
            self.send_error(413, "Request entity too large")
            return
        
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            story_content = data.get('content', '')
            
            # Parse and validate
            compiler = StoryCompiler()
            story = compiler.parse(story_content)
            errors = compiler.validate(story)
            
            self.send_json_response({
                'valid': len(errors) == 0,
                'errors': errors,
                'sections': len(story.sections),
                'title': story.metadata.title,
                'author': story.metadata.author
            })
        
        except Exception as e:
            self.send_json_response({
                'valid': False,
                'errors': [str(e)]
            })
    
    def save_story(self):
        """Save a story from POST data."""
        content_length = int(self.headers['Content-Length'])
        
        # Limit request size to prevent DOS (10MB max)
        MAX_REQUEST_SIZE = 10 * 1024 * 1024
        if content_length > MAX_REQUEST_SIZE:
            self.send_error(413, "Request entity too large")
            return
        
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            story_content = data.get('content', '')
            filename = data.get('filename', 'new_story.txt')
            
            # Sanitize filename - allow only alphanumeric, dash, underscore, dot
            import re
            filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
            if not filename:
                filename = 'new_story.txt'
            
            # Ensure .txt extension
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            # Validate path safety
            is_safe, story_path = is_safe_path(self.stories_dir, filename)
            if not is_safe:
                self.send_error(403, "Invalid filename")
                return
            
            # Save to stories directory
            self.stories_dir.mkdir(parents=True, exist_ok=True)
            
            with open(story_path, 'w', encoding='utf-8') as f:
                f.write(story_content)
            
            self.send_json_response({
                'success': True,
                'message': f'Story saved as {filename}',
                'filename': filename
            })
        
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    def send_json_response(self, data: Any, status: int = 200):
        """Send a JSON response."""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        # Simple logging that works on older systems
        print(f"[{self.log_date_time_string()}] {format % args}")


def get_index_html() -> str:
    """Return the HTML for the main interface."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pick-a-Page Story Tool</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, Georgia, serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #333;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        /* Book Cover Header */
        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 8px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: 600;
        }
        
        .subtitle {
            font-size: 1.1em;
            opacity: 0.95;
            font-style: italic;
        }
        
        /* Book Container with Paper Texture */
        .book-container {
            background: linear-gradient(to right, #faf8f3 0%, #f5f3ee 50%, #faf8f3 100%);
            border-radius: 8px;
            box-shadow: 
                0 2px 3px rgba(0,0,0,0.1),
                0 4px 8px rgba(0,0,0,0.1),
                0 8px 16px rgba(0,0,0,0.1),
                0 16px 32px rgba(0,0,0,0.15),
                inset 0 0 0 1px rgba(255,255,255,0.5);
            position: relative;
            overflow: hidden;
        }
        
        /* Book spine effect */
        .book-container::before {
            content: '';
            position: absolute;
            left: 30px;
            top: 0;
            bottom: 0;
            width: 1px;
            background: linear-gradient(to bottom, 
                transparent 0%, 
                rgba(0,0,0,0.05) 5%, 
                rgba(0,0,0,0.05) 95%, 
                transparent 100%);
            box-shadow: 1px 0 3px rgba(0,0,0,0.08);
            z-index: 1;
        }
        
        /* Bookmark Tabs */
        .bookmark-tabs {
            display: flex;
            gap: 5px;
            padding: 0 40px;
            position: relative;
            z-index: 10;
        }
        
        .bookmark-tab {
            padding: 12px 24px;
            background: linear-gradient(to bottom, #d4c4b0 0%, #c8b89d 100%);
            border: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #5a4a3a;
            transition: all 0.3s ease;
            position: relative;
            box-shadow: 
                0 -2px 4px rgba(0,0,0,0.1),
                inset 0 1px 0 rgba(255,255,255,0.3);
            font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, Georgia, serif;
        }
        
        .bookmark-tab:hover:not(.active) {
            background: linear-gradient(to bottom, #ddd0bc 0%, #d1c2ad 100%);
            transform: translateY(-2px);
        }
        
        .bookmark-tab.active {
            background: linear-gradient(to right, #faf8f3 0%, #f5f3ee 50%, #faf8f3 100%);
            color: #667eea;
            box-shadow: none;
            cursor: default;
        }
        
        .bookmark-tab.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(to right, #faf8f3 0%, #f5f3ee 50%, #faf8f3 100%);
        }
        
        /* Page Content */
        .page-content {
            padding: 50px 60px;
            min-height: 500px;
            position: relative;
            background: linear-gradient(to right, #faf8f3 0%, #f5f3ee 50%, #faf8f3 100%);
        }
        
        .view {
            display: none;
        }
        
        .view.active {
            display: block;
            animation: fadeIn 0.4s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Story Library View */
        .page-title {
            font-size: 2.2em;
            color: #667eea;
            margin-bottom: 30px;
            font-weight: 600;
            text-align: center;
            border-bottom: 2px solid rgba(102, 126, 234, 0.2);
            padding-bottom: 15px;
        }
        
        .story-list {
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 30px;
        }
        
        .story-item {
            padding: 20px;
            margin-bottom: 15px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
            border-left: 4px solid #667eea;
        }
        
        .story-item:hover {
            background: rgba(255, 255, 255, 0.9);
            border-color: #667eea;
            transform: translateX(8px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        }
        
        .story-item.selected {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #5568d3;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .story-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .story-meta {
            font-size: 0.95em;
            opacity: 0.85;
        }
        
        /* Buttons */
        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin-top: 30px;
        }
        
        .btn {
            display: inline-block;
            padding: 14px 28px;
            font-size: 1.05em;
            font-weight: 600;
            text-align: center;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }
        
        .btn-secondary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(72, 187, 120, 0.4);
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
            color: white;
        }
        
        .btn-warning:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(246, 173, 85, 0.4);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        /* Editor View */
        .editor-container {
            margin-top: 20px;
        }
        
        textarea {
            width: 100%;
            min-height: 350px;
            padding: 20px;
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.6;
            border: 2px solid rgba(102, 126, 234, 0.2);
            border-radius: 8px;
            resize: vertical;
            background: rgba(255, 255, 255, 0.7);
            color: #2c3e50;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Messages */
        .message {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
            font-size: 0.95em;
        }
        
        .message.success {
            background: rgba(198, 246, 213, 0.9);
            color: #22543d;
            border: 1px solid #9ae6b4;
        }
        
        .message.error {
            background: rgba(254, 215, 215, 0.9);
            color: #742a2a;
            border: 1px solid #fc8181;
        }
        
        .message.info {
            background: rgba(190, 227, 248, 0.9);
            color: #2c5282;
            border: 1px solid #90cdf4;
        }
        
        /* Loading spinner */
        .loading {
            display: none;
            text-align: center;
            padding: 40px 20px;
        }
        
        .spinner {
            border: 4px solid rgba(102, 126, 234, 0.1);
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        
        .empty-state p {
            font-size: 1.1em;
            margin: 10px 0;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            body {
                padding: 20px 10px;
            }
            
            h1 {
                font-size: 2em;
            }
            
            .book-container::before {
                left: 20px;
            }
            
            .bookmark-tabs {
                padding: 0 20px;
                gap: 3px;
            }
            
            .bookmark-tab {
                padding: 10px 16px;
                font-size: 0.9em;
            }
            
            .page-content {
                padding: 30px 25px;
            }
            
            .page-title {
                font-size: 1.8em;
            }
            
            .story-item {
                padding: 15px;
            }
            
            textarea {
                min-height: 250px;
                font-size: 13px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📖 Pick-a-Page</h1>
            <p class="subtitle">Create and play your own adventure stories</p>
        </header>
        
        <div class="book-container">
            <!-- Bookmark Tabs -->
            <div class="bookmark-tabs">
                <button class="bookmark-tab active" data-view="library">📚 Story Library</button>
                <button class="bookmark-tab" data-view="editor">✏️ Story Editor</button>
                <button class="bookmark-tab" data-view="player" style="display: none;">📖 Story Player</button>
            </div>
            
            <!-- Page Content -->
            <div class="page-content">
                <!-- Library View -->
                <div id="libraryView" class="view active">
                    <h2 class="page-title">Story Library</h2>
                    <div id="storyList" class="story-list">
                        <div class="loading">
                            <div class="spinner"></div>
                            <p>Loading stories...</p>
                        </div>
                    </div>
                    <div class="actions">
                        <button id="playBtn" class="btn btn-primary" disabled>▶️ Play Story</button>
                        <button id="editBtn" class="btn btn-secondary" disabled>✏️ Edit Story</button>
                        <button id="newBtn" class="btn btn-warning">➕ New Story</button>
                    </div>
                </div>
                
                <!-- Editor View -->
                <div id="editorView" class="view">
                    <h2 id="editorTitle" class="page-title">Story Editor</h2>
                    <div id="message" class="message"></div>
                    <div class="editor-container">
                        <textarea id="editor" placeholder="Write your story here...

Example format:

---
title: My Adventure
author: Your Name
---

[[beginning]]

You wake up in a mysterious place...

[[Explore]]
[[Go back to sleep]]

---

[[Explore]]

You discover something amazing!

[[Continue the adventure]]"></textarea>
                    </div>
                    <div class="actions">
                        <button id="validateBtn" class="btn btn-secondary">✓ Validate</button>
                        <button id="saveBtn" class="btn btn-secondary">💾 Save</button>
                        <button id="compileBtn" class="btn btn-primary">🚀 Compile & Play</button>
                    </div>
                </div>
                
                <!-- Player View -->
                <div id="playerView" class="view">
                    <div class="actions" style="margin-bottom: 20px;">
                        <button id="backToLibraryBtn" class="btn btn-secondary">← Back to Library</button>
                    </div>
                    <iframe id="storyFrame" sandbox="allow-scripts allow-same-origin" style="width: 100%; min-height: 600px; border: 2px solid rgba(102, 126, 234, 0.2); border-radius: 8px; background: white;"></iframe>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let selectedStory = null;
        let stories = [];
        
        // Tab switching
        document.addEventListener('DOMContentLoaded', () => {
            // Bookmark tab navigation
            document.querySelectorAll('.bookmark-tab').forEach(tab => {
                tab.addEventListener('click', () => switchTab(tab.dataset.view));
            });
            
            // Load stories on page load
            loadStories();
            
            // Event listeners for buttons
            document.getElementById('playBtn').addEventListener('click', playStory);
            document.getElementById('editBtn').addEventListener('click', editStory);
            document.getElementById('newBtn').addEventListener('click', newStory);
            document.getElementById('validateBtn').addEventListener('click', validateStory);
            document.getElementById('saveBtn').addEventListener('click', saveStory);
            document.getElementById('compileBtn').addEventListener('click', compileStory);
            document.getElementById('backToLibraryBtn').addEventListener('click', () => switchTab('library'));
        });
        
        function switchTab(viewName) {
            // Update tab active states
            document.querySelectorAll('.bookmark-tab').forEach(tab => {
                tab.classList.toggle('active', tab.dataset.view === viewName);
            });
            
            // Update view active states
            document.querySelectorAll('.view').forEach(view => {
                view.classList.remove('active');
            });
            
            if (viewName === 'library') {
                document.getElementById('libraryView').classList.add('active');
                // Hide player tab when going back to library
                document.querySelector('[data-view="player"]').style.display = 'none';
            } else if (viewName === 'editor') {
                document.getElementById('editorView').classList.add('active');
            } else if (viewName === 'player') {
                document.getElementById('playerView').classList.add('active');
                // Show player tab
                document.querySelector('[data-view="player"]').style.display = 'block';
            }
        }
        
        async function loadStories() {
            const listEl = document.getElementById('storyList');
            listEl.querySelector('.loading').style.display = 'block';
            
            try {
                const response = await fetch('/api/stories');
                stories = await response.json();
                
                listEl.innerHTML = '';
                
                if (stories.length === 0) {
                    listEl.innerHTML = `
                        <div class="empty-state">
                            <p>No stories found.</p>
                            <p>Click "New Story" to create one!</p>
                        </div>
                    `;
                } else {
                    stories.forEach(story => {
                        const item = document.createElement('div');
                        item.className = 'story-item';
                        item.innerHTML = `
                            <div class="story-title">${story.title}</div>
                            <div class="story-meta">by ${story.author} • ${story.sections || '?'} sections</div>
                        `;
                        item.addEventListener('click', () => selectStory(story, item));
                        listEl.appendChild(item);
                    });
                }
            } catch (error) {
                showMessage('Error loading stories: ' + error.message, 'error');
            }
        }
        
        function selectStory(story, element) {
            // Deselect previous
            document.querySelectorAll('.story-item').forEach(el => {
                el.classList.remove('selected');
            });
            
            // Select new
            element.classList.add('selected');
            selectedStory = story;
            
            // Enable buttons
            document.getElementById('playBtn').disabled = false;
            document.getElementById('editBtn').disabled = false;
        }
        
        async function playStory() {
            if (!selectedStory) return;
            
            showMessage('Compiling story...', 'info');
            
            try {
                // Load story content
                const response = await fetch(`/api/story/${selectedStory.filename}`);
                const data = await response.json();
                
                // Compile it
                const compileResponse = await fetch('/api/compile', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        content: data.content,
                        filename: selectedStory.filename
                    })
                });
                
                const result = await compileResponse.json();
                
                if (result.success) {
                    // Load in iframe and switch to player tab
                    document.getElementById('storyFrame').src = result.play_url;
                    switchTab('player');
                    showMessage('Story loaded!', 'success');
                } else {
                    showMessage('Compilation errors: ' + result.errors.join(', '), 'error');
                }
            } catch (error) {
                showMessage('Error: ' + error.message, 'error');
            }
        }
        
        async function editStory() {
            if (!selectedStory) return;
            
            try {
                const response = await fetch(`/api/story/${selectedStory.filename}`);
                const data = await response.json();
                
                document.getElementById('editor').value = data.content;
                document.getElementById('editorTitle').textContent = `Editing: ${selectedStory.title}`;
                switchTab('editor');
                showMessage(`Loaded ${selectedStory.filename} for editing`, 'success');
            } catch (error) {
                showMessage('Error loading story: ' + error.message, 'error');
            }
        }
        
        function newStory() {
            document.getElementById('editor').value = `---
title: My New Adventure
author: Your Name
---

[[beginning]]

Write your story here...

[[Make a choice]]

---

[[Make a choice]]

Continue your adventure!
`;
            document.getElementById('editorTitle').textContent = 'New Story';
            selectedStory = null;
            switchTab('editor');
            showMessage('Ready to create a new story!', 'info');
        }
        
        async function validateStory() {
            const content = document.getElementById('editor').value;
            
            if (!content.trim()) {
                showMessage('Editor is empty!', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/validate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content})
                });
                
                const result = await response.json();
                
                if (result.valid) {
                    showMessage(`✓ Story is valid! ${result.sections} sections found.`, 'success');
                } else {
                    showMessage('Validation errors: ' + result.errors.join(', '), 'error');
                }
            } catch (error) {
                showMessage('Error: ' + error.message, 'error');
            }
        }
        
        async function saveStory() {
            const content = document.getElementById('editor').value;
            
            if (!content.trim()) {
                showMessage('Editor is empty!', 'error');
                return;
            }
            
            const filename = prompt('Save as:', selectedStory?.filename || 'my_story.txt');
            if (!filename) return;
            
            try {
                const response = await fetch('/api/save', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content, filename})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage(`Saved as ${result.filename}!`, 'success');
                    loadStories(); // Refresh list
                } else {
                    showMessage('Error: ' + result.error, 'error');
                }
            } catch (error) {
                showMessage('Error: ' + error.message, 'error');
            }
        }
        
        async function compileStory() {
            const content = document.getElementById('editor').value;
            
            if (!content.trim()) {
                showMessage('Editor is empty!', 'error');
                return;
            }
            
            showMessage('Compiling story...', 'info');
            
            try {
                const filename = selectedStory?.filename || 'compiled_story.txt';
                const response = await fetch('/api/compile', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content, filename})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Load in iframe and switch to player tab
                    document.getElementById('storyFrame').src = result.play_url;
                    switchTab('player');
                    showMessage('Story compiled and loaded!', 'success');
                } else {
                    showMessage('Compilation errors: ' + result.errors.join(', '), 'error');
                }
            } catch (error) {
                showMessage('Error: ' + error.message, 'error');
            }
        }
        
        function showMessage(text, type) {
            const msgEl = document.getElementById('message');
            msgEl.textContent = text;
            msgEl.className = `message ${type}`;
            msgEl.style.display = 'block';
            
            setTimeout(() => {
                msgEl.style.display = 'none';
            }, 5000);
        }
    </script>
</body>
</html>"""


def start_server(host: str = '0.0.0.0', port: int = 8000, 
                 stories_dir: Path = None, output_dir: Path = None):
    """
    Start the web server.
    
    Args:
        host: Host to bind to (0.0.0.0 for all interfaces, 127.0.0.1 for localhost)
        port: Port to listen on
        stories_dir: Directory containing story files
        output_dir: Directory for compiled HTML files
    """
    if stories_dir is None:
        stories_dir = Path.cwd() / 'examples'
    if output_dir is None:
        output_dir = Path.cwd() / 'output'
    
    # Ensure directories exist
    stories_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create handler with directory context
    def handler(*args, **kwargs):
        return StoryHandler(*args, stories_dir=stories_dir, 
                          output_dir=output_dir, **kwargs)
    
    with socketserver.TCPServer((host, port), handler) as httpd:
        print(f"\n🌐 Pick-a-Page server starting...")
        print(f"📁 Stories directory: {stories_dir.absolute()}")
        print(f"📁 Output directory: {output_dir.absolute()}")
        print(f"\n✨ Server running at:")
        print(f"   Local:   http://127.0.0.1:{port}")
        if host == '0.0.0.0':
            print(f"   Network: http://<your-ip>:{port}")
        print(f"\n👉 Open in browser: http://127.0.0.1:{port}")
        print(f"\n⛔ Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")
