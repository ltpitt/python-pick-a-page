"""
Tests for legacy browser support functionality.
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


class TestBrowserDetectionScript:
    """Test browser detection script is properly served."""
    
    def test_browser_detect_script_returns_200(self, client):
        """Browser detection script should be accessible."""
        response = client.get("/static/js/browser-detect.js")
        assert response.status_code == 200
    
    def test_browser_detect_script_contains_feature_detection(self, client):
        """Browser detection script should contain feature detection functions."""
        response = client.get("/static/js/browser-detect.js")
        content = response.data.decode('utf-8')
        
        # Should contain async/await detection
        assert 'supportsAsyncAwait' in content
        
        # Should contain object spread detection
        assert 'supportsObjectSpread' in content
        
        # Should contain fetch detection
        assert 'supportsFetch' in content
    
    def test_browser_detect_loads_legacy_or_modern_scripts(self, client):
        """Browser detection script should load appropriate scripts."""
        response = client.get("/static/js/browser-detect.js")
        content = response.data.decode('utf-8')
        
        # Should reference legacy scripts
        assert 'legacy/api-service-legacy.js' in content
        assert 'legacy/i18n-service-legacy.js' in content
        assert 'legacy/story-manager-legacy.js' in content
        assert 'legacy/ui-controller-legacy.js' in content
        assert 'legacy/app-legacy.js' in content
        
        # Should reference modern scripts
        assert 'api-service.js' in content
        assert 'i18n-service.js' in content
        assert 'story-manager.js' in content
        assert 'ui-controller.js' in content
        assert 'app.js' in content


class TestLegacyJavaScriptFiles:
    """Test legacy JavaScript files are accessible and valid."""
    
    def test_legacy_api_service_returns_200(self, client):
        """Legacy API service script should be accessible."""
        response = client.get("/static/js/legacy/api-service-legacy.js")
        assert response.status_code == 200
    
    def test_legacy_i18n_service_returns_200(self, client):
        """Legacy i18n service script should be accessible."""
        response = client.get("/static/js/legacy/i18n-service-legacy.js")
        assert response.status_code == 200
    
    def test_legacy_story_manager_returns_200(self, client):
        """Legacy story manager script should be accessible."""
        response = client.get("/static/js/legacy/story-manager-legacy.js")
        assert response.status_code == 200
    
    def test_legacy_ui_controller_returns_200(self, client):
        """Legacy UI controller script should be accessible."""
        response = client.get("/static/js/legacy/ui-controller-legacy.js")
        assert response.status_code == 200
    
    def test_legacy_app_returns_200(self, client):
        """Legacy app script should be accessible."""
        response = client.get("/static/js/legacy/app-legacy.js")
        assert response.status_code == 200
    
    def test_legacy_scripts_use_es5_syntax(self, client):
        """Legacy scripts should use ES5 compatible syntax (no async/await)."""
        legacy_files = [
            "/static/js/legacy/api-service-legacy.js",
            "/static/js/legacy/i18n-service-legacy.js",
            "/static/js/legacy/story-manager-legacy.js",
            "/static/js/legacy/ui-controller-legacy.js",
            "/static/js/legacy/app-legacy.js"
        ]
        
        for file_path in legacy_files:
            response = client.get(file_path)
            content = response.data.decode('utf-8')
            
            # Should NOT contain async function declarations (ES2017)
            # 'async function' is the actual syntax that breaks old browsers
            lines = content.split('\n')
            for line in lines:
                # Skip comment lines (lines that are primarily comments)
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('*'):
                    continue
                # Check for actual async function usage (not in comments)
                assert 'async function' not in line, f"Found 'async function' in {file_path}: {line}"
                # Check for async arrow functions
                assert 'async (' not in line, f"Found 'async (' in {file_path}: {line}"
                assert 'async(' not in line, f"Found 'async(' in {file_path}: {line}"
    
    def test_legacy_api_service_uses_promises(self, client):
        """Legacy API service should use Promises instead of async/await."""
        response = client.get("/static/js/legacy/api-service-legacy.js")
        content = response.data.decode('utf-8')
        
        # Should use .then() for Promise chains
        assert '.then(' in content
        
        # Should use Object.assign instead of spread
        assert 'Object.assign' in content


class TestModernJavaScriptFiles:
    """Test modern JavaScript files are still accessible."""
    
    def test_modern_api_service_returns_200(self, client):
        """Modern API service script should be accessible."""
        response = client.get("/static/js/api-service.js")
        assert response.status_code == 200
    
    def test_modern_app_returns_200(self, client):
        """Modern app script should be accessible."""
        response = client.get("/static/js/app.js")
        assert response.status_code == 200
    
    def test_modern_scripts_use_async_await(self, client):
        """Modern scripts should use async/await."""
        response = client.get("/static/js/api-service.js")
        content = response.data.decode('utf-8')
        
        # Modern version should use async/await
        assert 'async ' in content


class TestBaseTemplateIncludesBrowserDetect:
    """Test that base template includes browser detection script."""
    
    def test_index_page_includes_browser_detect(self, client):
        """Index page should include browser detection script."""
        response = client.get("/")
        content = response.data.decode('utf-8')
        
        # Should include browser-detect.js
        assert 'browser-detect.js' in content
        
        # Should NOT directly include other JS files (they are loaded dynamically)
        assert 'src="/static/js/api-service.js"' not in content
        assert 'src="/static/js/app.js"' not in content


class TestCSSFocusFallback:
    """Test that CSS has proper focus fallbacks."""
    
    def test_base_css_has_focus_fallback(self, client):
        """Base CSS should have :focus fallback for :focus-visible."""
        response = client.get("/static/css/base.css")
        content = response.data.decode('utf-8')
        
        # Should have both :focus and :focus-visible
        assert ':focus {' in content or '*:focus {' in content
        assert ':focus-visible' in content


class TestGeneratedStoryLegacyCompatibility:
    """Test that generated stories are compatible with legacy browsers."""
    
    def test_compiled_story_uses_var_declarations(self, client):
        """Compiled story JavaScript should use var instead of const for compatibility."""
        # First compile a story
        story_content = """---
title: Test Story
author: Test Author
---

[[beginning]]

This is a test story.

[[next]]

---

[[next]]

The end!
"""
        response = client.post("/api/compile", json={
            "content": story_content,
            "filename": "test_legacy_compat.txt"
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data.get("success") == True
        
        # Get the compiled story
        play_response = client.get(data.get("play_url"))
        html_content = play_response.data.decode('utf-8')
        
        # Check JavaScript uses var instead of const/let for better compatibility
        assert 'var ' in html_content
        
        # Check smooth scroll has fallback
        assert 'smoothScrollTo' in html_content
        assert 'scrollBehavior' in html_content
