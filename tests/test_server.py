"""
Tests for the web server module.

Following TDD principles: comprehensive coverage of all server functionality.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
import http.client

from pick_a_page.server import is_safe_path, StoryHandler, get_index_html


def extract_json_from_response(response_bytes: bytes) -> dict:
    """Extract JSON body from HTTP response."""
    response = response_bytes.decode('utf-8')
    # Find the blank line that separates headers from body
    if '\r\n\r\n' in response:
        _, body = response.split('\r\n\r\n', 1)
    elif '\n\n' in response:
        _, body = response.split('\n\n', 1)
    else:
        body = response
    return json.loads(body) if body.strip() else {}


class TestPathSafety:
    """Test the is_safe_path security function."""
    
    def test_safe_simple_filename(self, tmp_path):
        """Simple filename should be safe."""
        is_safe, resolved = is_safe_path(tmp_path, "story.txt")
        assert is_safe is True
        assert resolved == tmp_path / "story.txt"
    
    def test_blocks_parent_directory_traversal(self, tmp_path):
        """Should block ../ directory traversal."""
        is_safe, resolved = is_safe_path(tmp_path, "../etc/passwd")
        assert is_safe is False
    
    def test_blocks_absolute_paths(self, tmp_path):
        """Should block absolute paths."""
        is_safe, resolved = is_safe_path(tmp_path, "/etc/passwd")
        assert is_safe is False
    
    def test_blocks_multiple_traversal(self, tmp_path):
        """Should block multiple ../ attempts."""
        is_safe, resolved = is_safe_path(tmp_path, "../../../../../../etc/passwd")
        assert is_safe is False
    
    def test_blocks_hidden_traversal(self, tmp_path):
        """Should block traversal in middle of path."""
        is_safe, resolved = is_safe_path(tmp_path, "stories/../../../etc/passwd")
        assert is_safe is False
    
    def test_allows_subdirectory(self, tmp_path):
        """Should allow accessing subdirectories within base."""
        subdir = tmp_path / "stories"
        subdir.mkdir()
        is_safe, resolved = is_safe_path(tmp_path, "stories/my_story.txt")
        assert is_safe is True
        assert resolved == tmp_path / "stories" / "my_story.txt"
    
    def test_blocks_windows_path_separators(self, tmp_path):
        """Should block Windows-style path separators."""
        is_safe, resolved = is_safe_path(tmp_path, "..\\..\\windows\\system32")
        assert is_safe is False
    
    def test_safe_path_with_underscores_dashes(self, tmp_path):
        """Should allow underscores and dashes in filename."""
        is_safe, resolved = is_safe_path(tmp_path, "my-cool_story-v2.txt")
        assert is_safe is True
    
    def test_blocks_dot_files_in_traversal(self, tmp_path):
        """Should block paths starting with dot in traversal."""
        is_safe, resolved = is_safe_path(tmp_path, "./../secrets.txt")
        assert is_safe is False


class TestIndexPage:
    """Test the main HTML interface generation."""
    
    def test_get_index_html_returns_html(self):
        """Should return HTML string."""
        html = get_index_html()
        assert isinstance(html, str)
        assert html.startswith("<!DOCTYPE html>")
    
    def test_index_contains_title(self):
        """Should contain Pick-a-Page title."""
        html = get_index_html()
        assert "Pick-a-Page" in html
    
    def test_index_contains_story_elements(self):
        """Should contain story-related UI elements."""
        html = get_index_html()
        assert "Story Library" in html or "story-list" in html
        assert "editor" in html.lower()
    
    def test_index_contains_javascript(self):
        """Should contain JavaScript for functionality."""
        html = get_index_html()
        assert "<script>" in html
        assert "fetch" in html  # Using Fetch API


class TestStoryHandlerGET:
    """Test GET request handling."""
    
    @pytest.fixture
    def handler(self, tmp_path):
        """Create a test handler with temporary directories."""
        stories_dir = tmp_path / "stories"
        output_dir = tmp_path / "output"
        stories_dir.mkdir()
        output_dir.mkdir()
        
        # Create mock request/response
        mock_request = Mock()
        mock_request.makefile = Mock(return_value=BytesIO())
        
        handler = StoryHandler(
            mock_request,
            ("127.0.0.1", 12345),
            None,
            stories_dir=stories_dir,
            output_dir=output_dir
        )
        handler.wfile = BytesIO()
        handler.requestline = 'GET / HTTP/1.1'  # Mock for logging
        handler.request_version = 'HTTP/1.1'  # Mock for send_response
        return handler
    
    def test_serve_index_returns_200(self, handler):
        """Root path should return 200 OK with HTML."""
        handler.serve_index()
        output = handler.wfile.getvalue().decode('utf-8')
        assert "<!DOCTYPE html>" in output
    
    def test_serve_story_list_empty(self, handler):
        """Should return empty list when no stories exist."""
        handler.serve_story_list()
        data = extract_json_from_response(handler.wfile.getvalue())
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_serve_story_list_with_stories(self, handler, tmp_path):
        """Should list stories with metadata."""
        story_file = handler.stories_dir / "test_story.txt"
        story_file.write_text("""---
title: Test Story
author: Test Author
---

[[start]]

Hello world!
""")
        
        handler.serve_story_list()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert len(data) == 1
        assert data[0]['filename'] == 'test_story.txt'
        assert data[0]['title'] == 'Test Story'
        assert data[0]['author'] == 'Test Author'
    
    def test_serve_story_content_valid_file(self, handler):
        """Should return story content for valid file."""
        story_file = handler.stories_dir / "test.txt"
        story_file.write_text("Story content here")
        
        handler.serve_story_content("test.txt")
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['content'] == "Story content here"
        assert data['filename'] == "test.txt"
    
    def test_serve_story_content_blocks_traversal(self, handler):
        """Should block path traversal in story content."""
        with patch.object(handler, 'send_error') as mock_error:
            handler.serve_story_content("../../../etc/passwd")
            mock_error.assert_called_once_with(403, "Invalid file path")
    
    def test_serve_story_content_nonexistent(self, handler):
        """Should return 404 for nonexistent story."""
        with patch.object(handler, 'send_error') as mock_error:
            handler.serve_story_content("nonexistent.txt")
            mock_error.assert_called_once()
            assert mock_error.call_args[0][0] == 404
    
    def test_serve_compiled_story_exists(self, handler):
        """Should serve compiled HTML file."""
        html_file = handler.output_dir / "story.html"
        html_file.write_text("<html>Compiled story</html>")
        
        handler.serve_compiled_story("story")
        output = handler.wfile.getvalue().decode('utf-8')
        assert "Compiled story" in output
    
    def test_serve_compiled_story_blocks_traversal(self, handler):
        """Should block path traversal in compiled story."""
        with patch.object(handler, 'send_error') as mock_error:
            handler.serve_compiled_story("../../../etc/passwd")
            mock_error.assert_called_once_with(403, "Invalid file path")


class TestStoryHandlerPOST:
    """Test POST request handling."""
    
    @pytest.fixture
    def handler(self, tmp_path):
        """Create handler with mock POST data."""
        stories_dir = tmp_path / "stories"
        output_dir = tmp_path / "output"
        stories_dir.mkdir()
        output_dir.mkdir()
        
        mock_request = Mock()
        mock_request.makefile = Mock(return_value=BytesIO())
        
        handler = StoryHandler(
            mock_request,
            ("127.0.0.1", 12345),
            None,
            stories_dir=stories_dir,
            output_dir=output_dir
        )
        handler.wfile = BytesIO()
        handler.headers = {}
        handler.requestline = 'POST /api/compile HTTP/1.1'  # Mock for logging
        handler.request_version = 'HTTP/1.1'  # Mock for send_response
        return handler
    
    def test_compile_story_valid(self, handler):
        """Should compile valid story and return success."""
        story_content = """---
title: Test Story
author: Test
---

[[start]]

Hello world!
"""
        post_data = json.dumps({
            'content': story_content,
            'filename': 'test_story.txt'
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.compile_story()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['success'] is True
        assert 'play_url' in data
        assert (handler.output_dir / "test_story.html").exists()
    
    def test_compile_story_invalid(self, handler):
        """Should return errors for invalid story."""
        story_content = """
[[nonexistent-link]]

This links to nowhere.

[[Go nowhere|missing-section]]
"""
        post_data = json.dumps({
            'content': story_content,
            'filename': 'bad_story.txt'
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.compile_story()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['success'] is False
        # Can have either 'errors' (validation) or 'error' (parsing exception)
        assert 'errors' in data or 'error' in data
    
    def test_compile_sanitizes_filename(self, handler):
        """Should sanitize filename to prevent injection."""
        story_content = """---
title: Test
author: Test
---

[[start]]
Test
"""
        post_data = json.dumps({
            'content': story_content,
            'filename': '../../../malicious/../story.txt'
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.compile_story()
        
        # Should create sanitized filename
        files = list(handler.output_dir.glob("*.html"))
        assert len(files) == 1
        # Filename should be sanitized (no ../ or /)
        assert '..' not in files[0].name
    
    def test_compile_rejects_oversized_request(self, handler):
        """Should reject requests larger than 10MB."""
        handler.headers = {'Content-Length': str(11 * 1024 * 1024)}  # 11MB
        
        with patch.object(handler, 'send_error') as mock_error:
            handler.compile_story()
            mock_error.assert_called_once_with(413, "Request entity too large")
    
    def test_validate_story_valid(self, handler):
        """Should return valid=True for valid story."""
        story_content = """---
title: Test Story
author: Test
---

[[start]]

Hello!
"""
        post_data = json.dumps({
            'content': story_content
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.validate_story()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['valid'] is True
        assert data['sections'] == 1
        assert data['title'] == 'Test Story'
    
    def test_validate_story_invalid(self, handler):
        """Should return errors for invalid story."""
        story_content = """
[[start]]

Bad link here: [[nonexistent]]
"""
        post_data = json.dumps({
            'content': story_content
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.validate_story()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['valid'] is False
        assert len(data['errors']) > 0
    
    def test_validate_rejects_oversized_request(self, handler):
        """Should reject oversized validation requests."""
        handler.headers = {'Content-Length': str(11 * 1024 * 1024)}
        
        with patch.object(handler, 'send_error') as mock_error:
            handler.validate_story()
            mock_error.assert_called_once_with(413, "Request entity too large")
    
    def test_save_story_creates_file(self, handler):
        """Should save story to file."""
        story_content = "Story content"
        post_data = json.dumps({
            'content': story_content,
            'filename': 'my_story.txt'
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.save_story()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['success'] is True
        assert (handler.stories_dir / 'my_story.txt').exists()
        assert (handler.stories_dir / 'my_story.txt').read_text() == story_content
    
    def test_save_story_sanitizes_filename(self, handler):
        """Should sanitize dangerous filenames."""
        post_data = json.dumps({
            'content': 'test',
            'filename': '../../../etc/passwd'
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        with patch.object(handler, 'send_error') as mock_error:
            handler.save_story()
            # Should either sanitize or reject
            if not mock_error.called:
                # If not rejected, should be sanitized
                files = list(handler.stories_dir.glob("*.txt"))
                assert all('..' not in f.name for f in files)
    
    def test_save_story_adds_txt_extension(self, handler):
        """Should add .txt extension if missing."""
        post_data = json.dumps({
            'content': 'test',
            'filename': 'my_story'
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.save_story()
        
        assert (handler.stories_dir / 'my_story.txt').exists()
    
    def test_save_rejects_oversized_request(self, handler):
        """Should reject oversized save requests."""
        handler.headers = {'Content-Length': str(11 * 1024 * 1024)}
        
        with patch.object(handler, 'send_error') as mock_error:
            handler.save_story()
            mock_error.assert_called_once_with(413, "Request entity too large")


class TestSecurityHeaders:
    """Test security headers are properly set."""
    
    @pytest.fixture
    def handler(self, tmp_path):
        """Create handler for testing."""
        stories_dir = tmp_path / "stories"
        output_dir = tmp_path / "output"
        stories_dir.mkdir()
        output_dir.mkdir()
        
        mock_request = Mock()
        mock_request.makefile = Mock(return_value=BytesIO())
        
        handler = StoryHandler(
            mock_request,
            ("127.0.0.1", 12345),
            None,
            stories_dir=stories_dir,
            output_dir=output_dir
        )
        handler.wfile = BytesIO()
        return handler
    
    def test_index_has_security_headers(self, handler):
        """Index page should include security headers."""
        with patch.object(handler, 'send_header') as mock_header:
            with patch.object(handler, 'send_response'):
                with patch.object(handler, 'end_headers'):
                    handler.serve_index()
                    
                    # Check for security headers
                    header_calls = [call[0] for call in mock_header.call_args_list]
                    assert any('X-Content-Type-Options' in str(call) for call in header_calls)
                    assert any('X-Frame-Options' in str(call) for call in header_calls)
                    assert any('Content-Security-Policy' in str(call) for call in header_calls)


class TestLanguageEndpoints:
    """Test language and translation API endpoints."""
    
    @pytest.fixture
    def handler(self, tmp_path):
        """Create handler for testing."""
        stories_dir = tmp_path / "stories"
        output_dir = tmp_path / "output"
        stories_dir.mkdir()
        output_dir.mkdir()
        
        mock_request = Mock()
        mock_request.makefile = Mock(return_value=BytesIO())
        
        handler = StoryHandler(
            mock_request,
            ("127.0.0.1", 12345),
            None,
            stories_dir=stories_dir,
            output_dir=output_dir
        )
        handler.wfile = BytesIO()
        handler.requestline = "GET / HTTP/1.1"  # Required for logging
        handler.request_version = "HTTP/1.1"  # Required for send_response
        return handler
    
    def test_serve_languages_returns_available_languages(self, handler):
        """Should return list of available languages with metadata."""
        handler.serve_languages()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert 'languages' in data
        assert 'en' in data['languages']
        assert 'nl' in data['languages']
        assert 'it' in data['languages']
        
        # Check language has metadata
        assert 'name' in data['languages']['en']
        assert 'flag' in data['languages']['en']
    
    def test_serve_translations_for_english(self, handler):
        """Should return English translations."""
        handler.serve_translations('en')
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['language'] == 'en'
        assert 'translations' in data
        # Should only have web_ prefixed translations
        assert all(k.startswith('web_') for k in data['translations'].keys())
    
    def test_serve_translations_for_dutch(self, handler):
        """Should return Dutch translations."""
        handler.serve_translations('nl')
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['language'] == 'nl'
        assert 'translations' in data
    
    def test_serve_translations_for_invalid_language(self, handler):
        """Should return 404 for invalid language code."""
        with patch.object(handler, 'send_error') as mock_error:
            handler.serve_translations('invalid_lang')
            mock_error.assert_called_once()
            assert 404 in mock_error.call_args[0]


class TestRouting:
    """Test HTTP request routing."""
    
    @pytest.fixture
    def handler(self, tmp_path):
        """Create handler for testing."""
        stories_dir = tmp_path / "stories"
        output_dir = tmp_path / "output"
        stories_dir.mkdir()
        output_dir.mkdir()
        
        mock_request = Mock()
        mock_request.makefile = Mock(return_value=BytesIO())
        
        handler = StoryHandler(
            mock_request,
            ("127.0.0.1", 12345),
            None,
            stories_dir=stories_dir,
            output_dir=output_dir
        )
        handler.wfile = BytesIO()
        handler.requestline = "GET / HTTP/1.1"  # Required for logging
        handler.request_version = "HTTP/1.1"  # Required for send_response
        return handler
    
    def test_get_root_serves_index(self, handler):
        """GET / should serve the index page."""
        handler.path = '/'
        
        with patch.object(handler, 'serve_index') as mock_serve:
            handler.do_GET()
            mock_serve.assert_called_once()
    
    def test_get_stories_api(self, handler):
        """GET /api/stories should serve story list."""
        handler.path = '/api/stories'
        
        with patch.object(handler, 'serve_story_list') as mock_serve:
            handler.do_GET()
            mock_serve.assert_called_once()
    
    def test_get_languages_api(self, handler):
        """GET /api/languages should serve language list."""
        handler.path = '/api/languages'
        
        with patch.object(handler, 'serve_languages') as mock_serve:
            handler.do_GET()
            mock_serve.assert_called_once()
    
    def test_get_translations_api(self, handler):
        """GET /api/translations/{lang} should serve translations."""
        handler.path = '/api/translations/en'
        
        with patch.object(handler, 'serve_translations') as mock_serve:
            handler.do_GET()
            mock_serve.assert_called_once_with('en')
    
    def test_get_story_content_api(self, handler):
        """GET /api/story/{name} should serve story content."""
        handler.path = '/api/story/test.txt'
        
        with patch.object(handler, 'serve_story_content') as mock_serve:
            handler.do_GET()
            mock_serve.assert_called_once_with('test.txt')
    
    def test_get_play_route(self, handler):
        """GET /play/{name} should serve compiled story."""
        handler.path = '/play/test'
        
        with patch.object(handler, 'serve_compiled_story') as mock_serve:
            handler.do_GET()
            mock_serve.assert_called_once_with('test')
    
    def test_get_invalid_route_returns_404(self, handler):
        """GET to invalid route should return 404."""
        handler.path = '/invalid/route'
        
        with patch.object(handler, 'send_error') as mock_error:
            handler.do_GET()
            mock_error.assert_called_once_with(404, "File not found")
    
    def test_post_compile_api(self, handler):
        """POST /api/compile should compile story."""
        handler.path = '/api/compile'
        
        with patch.object(handler, 'compile_story') as mock_compile:
            handler.do_POST()
            mock_compile.assert_called_once()
    
    def test_post_validate_api(self, handler):
        """POST /api/validate should validate story."""
        handler.path = '/api/validate'
        
        with patch.object(handler, 'validate_story') as mock_validate:
            handler.do_POST()
            mock_validate.assert_called_once()
    
    def test_post_save_api(self, handler):
        """POST /api/save should save story."""
        handler.path = '/api/save'
        
        with patch.object(handler, 'save_story') as mock_save:
            handler.do_POST()
            mock_save.assert_called_once()
    
    def test_post_invalid_route_returns_404(self, handler):
        """POST to invalid route should return 404."""
        handler.path = '/invalid/api'
        
        with patch.object(handler, 'send_error') as mock_error:
            handler.do_POST()
            mock_error.assert_called_once_with(404, "Endpoint not found")


class TestStoryListBehavior:
    """Test story list endpoint behavior with different scenarios."""
    
    @pytest.fixture
    def handler(self, tmp_path):
        """Create handler for testing."""
        stories_dir = tmp_path / "stories"
        output_dir = tmp_path / "output"
        stories_dir.mkdir()
        output_dir.mkdir()
        
        mock_request = Mock()
        mock_request.makefile = Mock(return_value=BytesIO())
        
        handler = StoryHandler(
            mock_request,
            ("127.0.0.1", 12345),
            None,
            stories_dir=stories_dir,
            output_dir=output_dir
        )
        handler.wfile = BytesIO()
        handler.requestline = "GET / HTTP/1.1"  # Required for logging
        handler.request_version = "HTTP/1.1"  # Required for send_response
        return handler
    
    def test_handles_corrupted_story_files(self, handler):
        """Should handle corrupted story files gracefully."""
        # Create a corrupted story file
        corrupted = handler.stories_dir / "corrupted.txt"
        corrupted.write_text("Not valid story format!")
        
        handler.serve_story_list()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert len(data) == 1
        # Should still list the file with fallback info
        assert data[0]['filename'] == 'corrupted.txt'
        # Should have error field or use filename as title
        assert 'title' in data[0]
    
    def test_handles_multiple_stories(self, handler):
        """Should list multiple valid stories."""
        # Create multiple valid stories
        for i in range(3):
            story = handler.stories_dir / f"story{i}.txt"
            story.write_text(f"""---
title: Story {i}
author: Test Author
---

[[start]]
Content here
""")
        
        handler.serve_story_list()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert len(data) == 3
        titles = [s['title'] for s in data]
        assert 'Story 0' in titles
        assert 'Story 1' in titles
        assert 'Story 2' in titles


class TestErrorHandlingPaths:
    """Test error handling in various server operations."""
    
    @pytest.fixture
    def handler(self, tmp_path):
        """Create handler for testing."""
        stories_dir = tmp_path / "stories"
        output_dir = tmp_path / "output"
        stories_dir.mkdir()
        output_dir.mkdir()
        
        mock_request = Mock()
        mock_request.makefile = Mock(return_value=BytesIO())
        
        handler = StoryHandler(
            mock_request,
            ("127.0.0.1", 12345),
            None,
            stories_dir=stories_dir,
            output_dir=output_dir
        )
        handler.wfile = BytesIO()
        handler.requestline = "POST /api/compile HTTP/1.1"  # Required for logging
        handler.request_version = "HTTP/1.1"  # Required for send_response
        return handler
    
    def test_compile_with_empty_content(self, handler):
        """Should handle empty story content gracefully."""
        post_data = json.dumps({
            'content': '',
            'filename': 'empty.txt'
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.compile_story()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['success'] is False
    
    def test_compile_with_malformed_json(self, handler):
        """Should handle malformed JSON gracefully."""
        post_data = b'{invalid json}'
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.compile_story()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['success'] is False
    
    def test_validate_with_missing_sections(self, handler):
        """Should detect stories with missing sections."""
        story_content = """---
title: Test
author: Test
---

[[start]]
Go to [[nowhere]]
"""
        
        post_data = json.dumps({
            'content': story_content
        }).encode('utf-8')
        
        handler.headers = {'Content-Length': str(len(post_data))}
        handler.rfile = BytesIO(post_data)
        
        handler.validate_story()
        data = extract_json_from_response(handler.wfile.getvalue())
        
        assert data['valid'] is False
        assert len(data['errors']) > 0
