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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .story-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .story-item {
            padding: 15px;
            margin-bottom: 10px;
            background: #f7f7f7;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        
        .story-item:hover {
            background: #e9ecef;
            border-color: #667eea;
            transform: translateX(5px);
        }
        
        .story-item.selected {
            background: #667eea;
            color: white;
            border-color: #5568d3;
        }
        
        .story-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .story-meta {
            font-size: 0.9em;
            opacity: 0.7;
        }
        
        .btn {
            display: inline-block;
            padding: 15px 30px;
            font-size: 1.1em;
            font-weight: bold;
            text-align: center;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            margin: 5px;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #48bb78;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #38a169;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(72, 187, 120, 0.4);
        }
        
        .btn-warning {
            background: #f6ad55;
            color: white;
        }
        
        .btn-warning:hover {
            background: #ed8936;
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .editor-container {
            margin-top: 20px;
        }
        
        textarea {
            width: 100%;
            min-height: 300px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            resize: vertical;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            display: none;
        }
        
        .message.success {
            background: #c6f6d5;
            color: #22543d;
            border: 1px solid #9ae6b4;
        }
        
        .message.error {
            background: #fed7d7;
            color: #742a2a;
            border: 1px solid #fc8181;
        }
        
        .message.info {
            background: #bee3f8;
            color: #2c5282;
            border: 1px solid #90cdf4;
        }
        
        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        
        .empty-state svg {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
            opacity: 0.3;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📖 Pick-a-Page</h1>
            <p class="subtitle">Create and play your own adventure stories!</p>
        </header>
        
        <div class="main-content">
            <div class="card">
                <h2>📚 Story Library</h2>
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
            
            <div class="card">
                <h2 id="editorTitle">✨ Story Editor</h2>
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
        </div>
    </div>
    
    <script>
        let selectedStory = null;
        let stories = [];
        
        // Load stories on page load
        document.addEventListener('DOMContentLoaded', () => {
            loadStories();
            
            // Event listeners
            document.getElementById('playBtn').addEventListener('click', playStory);
            document.getElementById('editBtn').addEventListener('click', editStory);
            document.getElementById('newBtn').addEventListener('click', newStory);
            document.getElementById('validateBtn').addEventListener('click', validateStory);
            document.getElementById('saveBtn').addEventListener('click', saveStory);
            document.getElementById('compileBtn').addEventListener('click', compileStory);
        });
        
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
                    // Open in new window
                    window.open(result.play_url, '_blank');
                    showMessage('Story opened in new window!', 'success');
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
                document.getElementById('editorTitle').textContent = `✏️ Editing: ${selectedStory.title}`;
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
            document.getElementById('editorTitle').textContent = '✨ New Story';
            selectedStory = null;
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
                    window.open(result.play_url, '_blank');
                    showMessage('Story compiled and opened!', 'success');
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
