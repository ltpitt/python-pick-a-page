"""
Tests for story template/init functionality.
Following TDD approach - write tests first!
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.main import app

# Stories directory path
STORIES_DIR = Path(__file__).parent.parent.parent / "stories"

@pytest.fixture(scope="module", autouse=True)
def cleanup_template_test_stories():
    """Clean up template test stories before and after all tests in this module."""
    # List of test story filenames created by template tests
    test_stories = [
        "test_new_story.txt",
        "dutch_story.txt",
        "evil.txt",
        "story_no_ext.txt",
        "default_story.txt",
    ]
    
    def cleanup():
        """Remove test story files."""
        for filename in test_stories:
            story_path = STORIES_DIR / filename
            if story_path.exists():
                story_path.unlink()
    
    # Cleanup before tests
    cleanup()
    
    # Run tests
    yield
    
    # Cleanup after tests
    cleanup()

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

class TestTemplateEndpoint:
    """Test story template generation."""
    
    def test_get_template_returns_200(self, client):
        """Template endpoint should return 200 OK."""
        response = client.get("/api/template")
        assert response.status_code == 200
    
    def test_get_template_returns_story_structure(self, client):
        """Template should return valid story structure."""
        response = client.get("/api/template")
        data = response.json()
        
        assert "template" in data
        template = data["template"]
        
        # Should have metadata section
        assert "---" in template
        assert "title:" in template
        assert "author:" in template
        
        # Should have at least one section
        assert "[[" in template
        
    def test_get_template_with_language_returns_localized(self, client):
        """Template should support localization."""
        response = client.get("/api/template?lang=nl")
        assert response.status_code == 200
        data = response.json()
        
        # Should return template in requested language
        assert "template" in data
        
    def test_get_template_with_custom_title(self, client):
        """Template should allow custom title."""
        response = client.get("/api/template?title=My Adventure")
        assert response.status_code == 200
        data = response.json()
        template = data["template"]
        
        # Should include custom title
        assert "My Adventure" in template
    
    def test_get_template_with_custom_author(self, client):
        """Template should allow custom author."""
        response = client.get("/api/template?author=John Doe")
        assert response.status_code == 200
        data = response.json()
        template = data["template"]
        
        # Should include custom author
        assert "John Doe" in template
    
    def test_get_template_invalid_language_uses_english(self, client):
        """Invalid language should fall back to English."""
        response = client.get("/api/template?lang=invalid")
        assert response.status_code == 200
        # Should not error, just use default language

class TestNewStoryEndpoint:
    """Test creating new story with template."""
    
    def test_post_new_story_creates_file(self, client):
        """Should create new story file with template."""
        response = client.post("/api/new", json={
            "filename": "test_new_story.txt",
            "title": "Test Story",
            "author": "Test Author"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "filename" in data
        assert data["filename"] == "test_new_story.txt"
    
    def test_post_new_story_with_language(self, client):
        """Should create story with localized template."""
        response = client.post("/api/new", json={
            "filename": "dutch_story.txt",
            "title": "Mijn Verhaal",
            "author": "Test",
            "lang": "nl"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_post_new_story_sanitizes_filename(self, client):
        """Should sanitize dangerous filenames."""
        response = client.post("/api/new", json={
            "filename": "../../evil.txt",
            "title": "Test",
            "author": "Test"
        })
        
        # Should either reject or sanitize
        if response.status_code == 200:
            data = response.json()
            assert ".." not in data["filename"]
        else:
            assert response.status_code in [400, 403]
    
    def test_post_new_story_adds_txt_extension(self, client):
        """Should add .txt extension if missing."""
        response = client.post("/api/new", json={
            "filename": "story_no_ext",
            "title": "Test",
            "author": "Test"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"].endswith(".txt")
    
    def test_post_new_story_requires_filename(self, client):
        """Should require filename parameter."""
        response = client.post("/api/new", json={
            "title": "Test",
            "author": "Test"
        })
        
        assert response.status_code in [400, 422]
    
    def test_post_new_story_uses_defaults(self, client):
        """Should use default title/author if not provided."""
        response = client.post("/api/new", json={
            "filename": "default_story.txt"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

class TestCompileWithZip:
    """Test compile with ZIP creation (like CLI --no-zip flag)."""
    
    def test_compile_without_zip_flag_works(self, client):
        """Compile should work without ZIP flag (ZIP is optional)."""
        story_data = {
            "content": """---
title: ZIP Test
author: Test
---

[[start]]
Test story for ZIP.
""",
            "filename": "zip_test.txt"
        }
        
        response = client.post("/api/compile", json=story_data)
        assert response.status_code == 200
        data = response.json()
        
        # Should succeed even without ZIP
        assert data["success"] is True
        assert "play_url" in data

class TestBrowserOpen:
    """Test browser opening functionality (like CLI --no-open flag)."""
    
    def test_compile_with_no_open_flag(self, client):
        """Should support no-open flag to skip browser launch."""
        story_data = {
            "content": """---
title: Test
author: Test
---

[[start]]
Test.
""",
            "filename": "test.txt",
            "open_browser": False
        }
        
        response = client.post("/api/compile", json=story_data)
        assert response.status_code == 200
        # Should not attempt to open browser
