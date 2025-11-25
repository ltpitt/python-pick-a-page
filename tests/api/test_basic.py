"""
Tests for API endpoints - health, stories, compilation, i18n.
"""

import pytest
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.main import app

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check_returns_200(self, client):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_json(self, client):
        """Health endpoint should return JSON with status and version."""
        response = client.get("/health")
        data = response.get_json()
        assert "status" in data
        assert "version" in data
        assert data["status"] == "healthy"
        assert data["version"] == "2.0.0"

class TestLanguagesEndpoint:
    """Test i18n languages endpoint."""
    
    def test_get_languages_returns_200(self, client):
        """Languages endpoint should return 200 OK."""
        response = client.get("/api/languages")
        assert response.status_code == 200
    
    def test_get_languages_returns_all_15_languages(self, client):
        """Should return all 15 supported languages."""
        response = client.get("/api/languages")
        data = response.get_json()
        assert "languages" in data
        languages = data["languages"]
        assert len(languages) == 15
        
        # Check some specific languages
        assert "en" in languages
        assert "nl" in languages
        assert "it" in languages
        assert languages["en"]["name"] == "English"
        assert languages["nl"]["name"] == "Nederlands"

class TestTranslationsEndpoint:
    """Test i18n translations endpoint."""
    
    def test_get_translations_en_returns_200(self, client):
        """Translations endpoint should return 200 for English."""
        response = client.get("/api/translations/en")
        assert response.status_code == 200
    
    def test_get_translations_returns_web_keys_only(self, client):
        """Translations should only include web_* keys."""
        response = client.get("/api/translations/en")
        data = response.get_json()
        assert "translations" in data
        translations = data["translations"]
        
        # All keys should start with web_
        for key in translations.keys():
            assert key.startswith("web_")
        
        # Check some specific keys exist
        assert "web_tab_library" in translations
        assert "web_tab_editor" in translations
        assert "web_btn_play" in translations
    
    def test_get_translations_invalid_language_returns_404(self, client):
        """Invalid language should return 404."""
        response = client.get("/api/translations/invalid")
        assert response.status_code == 404

class TestStoriesEndpoint:
    """Test stories CRUD endpoints."""
    
    def test_list_stories_returns_200(self, client):
        """Stories list endpoint should return 200 OK."""
        response = client.get("/api/stories")
        assert response.status_code == 200
    
    def test_list_stories_returns_array(self, client):
        """Stories endpoint should return array of story objects."""
        response = client.get("/api/stories")
        data = response.get_json()
        assert isinstance(data, list)
        
        # If there are stories, check structure
        if len(data) > 0:
            story = data[0]
            assert "filename" in story
            assert "title" in story
            assert "author" in story
            assert "sections" in story
    
    def test_get_story_content_existing_file(self, client):
        """Should return content for existing story file."""
        # First get list of stories
        response = client.get("/api/stories")
        stories = response.get_json()
        
        if len(stories) > 0:
            filename = stories[0]["filename"]
            response = client.get(f"/api/story/{filename}")
            assert response.status_code == 200
            data = response.get_json()
            assert "content" in data
            assert "filename" in data
            assert data["filename"] == filename
    
    def test_get_story_content_nonexistent_file_returns_404(self, client):
        """Should return 404 for non-existent file."""
        response = client.get("/api/story/nonexistent_file.txt")
        assert response.status_code == 404
    
    def test_get_story_content_path_traversal_returns_403_or_404(self, client):
        """Should reject path traversal attempts with 403 or 404."""
        response = client.get("/api/story/../../../etc/passwd")
        # Could be 403 (forbidden) or 404 (not found after safe path check)
        assert response.status_code in [403, 404]

class TestCompileEndpoint:
    """Test story compilation endpoints."""
    
    def test_validate_valid_story_returns_200(self, client):
        """Validation should succeed for valid story."""
        valid_story = """---
title: Test Story
author: Test Author
---

[[start]]

This is the beginning.

[[Go forward]]

---

[[go-forward]]

You moved forward. The end!
"""
        response = client.post("/api/validate", json={"content": valid_story})
        assert response.status_code == 200
        data = response.get_json()
        assert data["valid"] is True
        assert len(data["errors"]) == 0
        assert data["title"] == "Test Story"
        assert data["author"] == "Test Author"
    
    def test_validate_invalid_story_returns_errors(self, client):
        """Validation should return errors for invalid story."""
        invalid_story = """---
title: Test Story
author: Test Author
---

[[start]]

Link to [[nonexistent]]
"""
        response = client.post("/api/validate", json={"content": invalid_story})
        assert response.status_code == 200
        data = response.get_json()
        assert data["valid"] is False
        assert len(data["errors"]) > 0

class TestPageEndpoint:
    """Test page rendering endpoint."""
    
    def test_index_page_returns_200(self, client):
        """Index page should return 200 OK."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_index_page_returns_html(self, client):
        """Index page should return HTML content."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.content_type
        assert b"Pick-a-Page" in response.data
