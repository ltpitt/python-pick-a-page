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
    html = """<!DOCTYPE html>
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
            color: #2c3e50;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        /* Book-style container */
        .book {
            background: #faf8f3;
            border-radius: 3px;
            box-shadow: 
                0 2px 3px rgba(0,0,0,0.1),
                0 4px 8px rgba(0,0,0,0.1),
                0 8px 16px rgba(0,0,0,0.1),
                0 16px 32px rgba(0,0,0,0.1),
                inset 0 0 0 1px rgba(255,255,255,0.5);
            position: relative;
            padding: 60px 70px 40px 70px;
            min-height: 600px;
        }
        
        /* Book spine effect */
        .book::before {
            content: '';
            position: absolute;
            left: 40px;
            top: 0;
            bottom: 0;
            width: 1px;
            background: linear-gradient(to bottom, 
                transparent 0%, 
                rgba(0,0,0,0.03) 5%, 
                rgba(0,0,0,0.03) 95%, 
                transparent 100%);
            box-shadow: 1px 0 2px rgba(0,0,0,0.05);
        }
        
        /* Bookmark tabs */
        .bookmarks {
            position: absolute;
            top: -20px;
            left: 50px;
            right: 50px;
            display: flex;
            gap: 10px;
            z-index: 10;
        }
        
        .bookmark {
            background: linear-gradient(to bottom, #e8d5b5 0%, #d4c1a0 100%);
            color: #5a4a3a;
            padding: 10px 25px 15px 25px;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
            border: 1px solid #c9b699;
            border-bottom: none;
            position: relative;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .bookmark:hover:not(.active) {
            background: linear-gradient(to bottom, #f0ddc5 0%, #dcc9a8 100%);
            transform: translateY(-2px);
        }
        
        .bookmark.active {
            background: #faf8f3;
            color: #8b6f47;
            box-shadow: 0 -3px 10px rgba(139, 111, 71, 0.2);
            border-color: #8b6f47;
            z-index: 11;
        }
        
        .bookmark::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-top: 5px solid transparent;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .bookmark.active::after {
            border-top-color: #8b6f47;
            opacity: 1;
        }
        
        /* Pages */
        .page {
            display: none;
            animation: pageFlip 0.5s ease-out;
        }
        
        .page.active {
            display: block;
        }
        
        @keyframes pageFlip {
            from { 
                opacity: 0; 
                transform: perspective(1000px) rotateY(-10deg);
            }
            to { 
                opacity: 1; 
                transform: perspective(1000px) rotateY(0deg);
            }
        }
        
        /* Page titles */
        .page-title {
            font-size: 2.5em;
            color: #8b6f47;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(139, 111, 71, 0.2);
            text-align: center;
        }
        
        /* Story Library styles */
        .story-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .story-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #e9ecef;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .story-card:hover {
            border-color: #667eea;
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }
        
        .story-card.selected {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }
        
        .story-card-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 8px;
            color: inherit;
        }
        
        .story-card.selected .story-card-title {
            color: white;
        }
        
        .story-card-meta {
            font-size: 0.9em;
            opacity: 0.7;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .story-actions {
            display: flex;
            gap: 15px;
            margin-top: 30px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        /* Editor styles */
        .editor-area {
            margin: 20px 0;
        }
        
        textarea {
            width: 100%;
            min-height: 400px;
            padding: 20px;
            font-family: 'Courier New', Monaco, monospace;
            font-size: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            resize: vertical;
            background: white;
            color: #2c3e50;
            line-height: 1.6;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            text-decoration: none;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover:not(:disabled)::before {
            left: 100%;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            box-shadow: 0 4px 6px rgba(72, 187, 120, 0.3);
        }
        
        .btn-secondary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(72, 187, 120, 0.4);
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
            color: white;
            box-shadow: 0 4px 6px rgba(246, 173, 85, 0.3);
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
        
        .btn:active:not(:disabled) {
            transform: translateY(0);
        }
        
        /* Messages */
        .message {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .message.success {
            background: #c6f6d5;
            color: #22543d;
            border-left: 4px solid #48bb78;
        }
        
        .message.error {
            background: #fed7d7;
            color: #742a2a;
            border-left: 4px solid #fc8181;
        }
        
        .message.info {
            background: #bee3f8;
            color: #2c5282;
            border-left: 4px solid #667eea;
        }
        
        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }
        
        .empty-state-icon {
            font-size: 4em;
            margin-bottom: 20px;
            opacity: 0.3;
        }
        
        /* Loading */
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            body {
                padding: 20px 10px;
            }
            
            .book {
                padding: 40px 30px 30px 30px;
            }
            
            .book::before {
                left: 20px;
            }
            
            .bookmarks {
                left: 20px;
                right: 20px;
                gap: 5px;
            }
            
            .bookmark {
                padding: 8px 15px 12px 15px;
                font-size: 14px;
            }
            
            .page-title {
                font-size: 2em;
            }
            
            .story-grid {
                grid-template-columns: 1fr;
            }
            
            .btn {
                padding: 12px 20px;
                font-size: 14px;
            }
        }
        
        /* Story player iframe */
        #storyPlayer {
            display: none;
            width: 100%;
            height: 600px;
            border: none;
            border-radius: 8px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="book">
            <!-- Bookmark navigation -->
            <div class="bookmarks">
                <div class="bookmark active" data-page="library">📚 Story Library</div>
                <div class="bookmark" data-page="editor">✏️ Story Editor</div>
                <div class="bookmark" id="playerBookmark" data-page="player" style="display: none;">📖 Story Reader</div>
            </div>
            
            <!-- Page: Story Library -->
            <div class="page active" id="page-library">
                <h1 class="page-title">📖 My Story Collection</h1>
                <div id="message" class="message"></div>
                
                <div id="storyList">
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Loading your stories...</p>
                    </div>
                </div>
                
                <div class="story-actions">
                    <button id="playBtn" class="btn btn-primary" disabled>
                        <span>▶️</span> Play Story
                    </button>
                    <button id="editLibraryBtn" class="btn btn-secondary" disabled>
                        <span>✏️</span> Edit Story
                    </button>
                    <button id="newStoryBtn" class="btn btn-warning">
                        <span>➕</span> New Story
                    </button>
                </div>
            </div>
            
            <!-- Page: Story Editor -->
            <div class="page" id="page-editor">
                <h1 class="page-title" id="editorTitle">✨ Create Your Story</h1>
                <div id="editorMessage" class="message"></div>
                
                <div class="editor-area">
                    <textarea id="storyEditor" placeholder="Write your adventure here...

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

You discover something amazing!"></textarea>
                </div>
                
                <div class="story-actions">
                    <button id="validateBtn" class="btn btn-secondary">
                        <span>✓</span> Validate
                    </button>
                    <button id="saveBtn" class="btn btn-secondary">
                        <span>💾</span> Save
                    </button>
                    <button id="compileBtn" class="btn btn-primary">
                        <span>🚀</span> Compile & Play
                    </button>
                </div>
            </div>
            
            <!-- Page: Story Player (hidden by default) -->
            <div class="page" id="page-player">
                <iframe id="storyPlayer"></iframe>
            </div>
        </div>
    </div>
    
    <script>
        let selectedStory = null;
        let stories = [];
        let currentEditingFilename = null;
        
        // Load stories on page load
        document.addEventListener('DOMContentLoaded', () => {
            loadStories();
            setupNavigation();
            setupEventListeners();
        });
        
        function setupNavigation() {
            document.querySelectorAll('.bookmark').forEach(bookmark => {
                bookmark.addEventListener('click', () => {
                    const targetPage = bookmark.dataset.page;
                    
                    // Keep player bookmark visible once a story is loaded
                    // This allows users to navigate between tabs and return to their story
                    
                    switchPage(targetPage);
                });
            });
        }
        
        function switchPage(pageName) {
            // Update bookmarks
            document.querySelectorAll('.bookmark').forEach(b => {
                b.classList.remove('active');
                if (b.dataset.page === pageName) {
                    b.classList.add('active');
                }
            });
            
            // Show/hide player bookmark
            const playerBookmark = document.getElementById('playerBookmark');
            if (pageName === 'player') {
                playerBookmark.style.display = 'block';
            }
            
            // Update pages
            document.querySelectorAll('.page').forEach(p => {
                p.classList.remove('active');
            });
            document.getElementById(`page-${pageName}`).classList.add('active');
        }
        
        function setupEventListeners() {
            document.getElementById('playBtn').addEventListener('click', playStory);
            document.getElementById('editLibraryBtn').addEventListener('click', () => {
                if (selectedStory) {
                    loadStoryForEditing(selectedStory);
                    switchPage('editor');
                }
            });
            document.getElementById('newStoryBtn').addEventListener('click', () => {
                newStory();
                switchPage('editor');
            });
            document.getElementById('validateBtn').addEventListener('click', validateStory);
            document.getElementById('saveBtn').addEventListener('click', saveStory);
            document.getElementById('compileBtn').addEventListener('click', compileAndPlay);
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
                            <div class="empty-state-icon">📚</div>
                            <h3>No stories yet</h3>
                            <p>Click "New Story" to create your first adventure!</p>
                        </div>
                    `;
                } else {
                    const grid = document.createElement('div');
                    grid.className = 'story-grid';
                    
                    stories.forEach(story => {
                        const card = document.createElement('div');
                        card.className = 'story-card';
                        card.innerHTML = `
                            <div class="story-card-title">${story.title}</div>
                            <div class="story-card-meta">by ${story.author}</div>
                            <div class="story-card-meta">${story.sections || '?'} sections</div>
                        `;
                        card.addEventListener('click', () => selectStory(story, card));
                        grid.appendChild(card);
                    });
                    
                    listEl.appendChild(grid);
                }
            } catch (error) {
                showMessage('Error loading stories: ' + error.message, 'error');
            }
        }
        
        function selectStory(story, element) {
            // Deselect all
            document.querySelectorAll('.story-card').forEach(c => c.classList.remove('selected'));
            
            // Select this one
            element.classList.add('selected');
            selectedStory = story;
            
            // Enable buttons
            document.getElementById('playBtn').disabled = false;
            document.getElementById('editLibraryBtn').disabled = false;
        }
        
        async function playStory() {
            if (!selectedStory) return;
            
            showMessage('Loading story...', 'info');
            
            try {
                // Load and compile
                const response = await fetch(`/api/story/${selectedStory.filename}`);
                const data = await response.json();
                
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
                    // Load in iframe
                    const iframe = document.getElementById('storyPlayer');
                    iframe.src = result.play_url;
                    iframe.style.display = 'block';
                    switchPage('player');
                } else {
                    showMessage('Errors: ' + (result.errors || [result.error]).join(', '), 'error');
                }
            } catch (error) {
                showMessage('Error: ' + error.message, 'error');
            }
        }
        
        async function loadStoryForEditing(story) {
            try {
                const response = await fetch(`/api/story/${story.filename}`);
                const data = await response.json();
                
                document.getElementById('storyEditor').value = data.content;
                document.getElementById('editorTitle').textContent = `✏️ Editing: ${story.title}`;
                currentEditingFilename = story.filename;
                showEditorMessage(`Loaded ${story.filename} for editing`, 'success');
            } catch (error) {
                showEditorMessage('Error loading story: ' + error.message, 'error');
            }
        }
        
        function newStory() {
            document.getElementById('storyEditor').value = `---
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
            document.getElementById('editorTitle').textContent = '✨ Create New Story';
            currentEditingFilename = null;
            showEditorMessage('Ready to write a new story!', 'info');
        }
        
        async function validateStory() {
            const content = document.getElementById('storyEditor').value;
            
            if (!content.trim()) {
                showEditorMessage('Editor is empty!', 'error');
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
                    showEditorMessage(`✓ Story is valid! Found ${result.sections} section(s).`, 'success');
                } else {
                    showEditorMessage('Validation errors: ' + (result.errors || [result.error]).join(', '), 'error');
                }
            } catch (error) {
                showEditorMessage('Error: ' + error.message, 'error');
            }
        }
        
        async function saveStory() {
            const content = document.getElementById('storyEditor').value;
            
            if (!content.trim()) {
                showEditorMessage('Editor is empty!', 'error');
                return;
            }
            
            const filename = prompt('Save as:', currentEditingFilename || 'my_story.txt');
            if (!filename) return;
            
            try {
                const response = await fetch('/api/save', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content, filename})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    currentEditingFilename = result.filename;
                    showEditorMessage(`✓ Saved as ${result.filename}!`, 'success');
                    loadStories(); // Refresh library
                } else {
                    showEditorMessage('Error: ' + (result.error || 'Unknown error'), 'error');
                }
            } catch (error) {
                showEditorMessage('Error: ' + error.message, 'error');
            }
        }
        
        async function compileAndPlay() {
            const content = document.getElementById('storyEditor').value;
            
            if (!content.trim()) {
                showEditorMessage('Editor is empty!', 'error');
                return;
            }
            
            showEditorMessage('Compiling story...', 'info');
            
            try {
                const filename = currentEditingFilename || 'preview_story.txt';
                const response = await fetch('/api/compile', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content, filename})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Load in iframe
                    const iframe = document.getElementById('storyPlayer');
                    iframe.src = result.play_url;
                    iframe.style.display = 'block';
                    switchPage('player');
                } else {
                    showEditorMessage('Compilation errors: ' + (result.errors || [result.error]).join(', '), 'error');
                }
            } catch (error) {
                showEditorMessage('Error: ' + error.message, 'error');
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
        
        function showEditorMessage(text, type) {
            const msgEl = document.getElementById('editorMessage');
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
    
    return html


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
