"""
Tests for the learning endpoints - tutorial and Markdown help.

These power the optional guided tutorial and the always-available
child-friendly Markdown reference required by the project's north star.
"""

import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.main import app
from backend.core.i18n import LANGUAGE_INFO
from backend.core.learning import get_tutorial, get_markdown_help


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestTutorialEndpoint:
    """Test the /api/tutorial endpoint."""

    def test_tutorial_returns_200(self, client):
        response = client.get("/api/tutorial")
        assert response.status_code == 200

    def test_tutorial_defaults_to_english(self, client):
        response = client.get("/api/tutorial")
        data = response.get_json()
        assert data["language"] == "en"

    def test_tutorial_has_five_steps(self, client):
        response = client.get("/api/tutorial")
        data = response.get_json()
        assert len(data["steps"]) == 5

    def test_tutorial_step_shape(self, client):
        response = client.get("/api/tutorial")
        step = response.get_json()["steps"][0]
        for key in ("step", "title", "body", "example"):
            assert key in step

    def test_tutorial_localized_for_italian(self, client):
        en = client.get("/api/tutorial?lang=en").get_json()["steps"][0]["title"]
        it = client.get("/api/tutorial?lang=it").get_json()["steps"][0]["title"]
        assert en != it

    def test_tutorial_unknown_language_falls_back_to_english(self, client):
        response = client.get("/api/tutorial?lang=xx")
        assert response.status_code == 200
        data = response.get_json()
        assert data["language"] == "en"
        assert len(data["steps"]) == 5


class TestMarkdownHelpEndpoint:
    """Test the /api/help/markdown endpoint."""

    def test_help_returns_200(self, client):
        response = client.get("/api/help/markdown")
        assert response.status_code == 200

    def test_help_has_six_items(self, client):
        response = client.get("/api/help/markdown")
        data = response.get_json()
        assert len(data["items"]) == 6

    def test_help_item_shape(self, client):
        response = client.get("/api/help/markdown")
        item = response.get_json()["items"][0]
        for key in ("id", "label", "syntax", "example", "hint"):
            assert key in item

    def test_help_localized_for_dutch(self, client):
        en = client.get("/api/help/markdown?lang=en").get_json()["items"][0]["label"]
        nl = client.get("/api/help/markdown?lang=nl").get_json()["items"][0]["label"]
        assert en != nl

    def test_help_unknown_language_falls_back_to_english(self, client):
        response = client.get("/api/help/markdown?lang=xx")
        assert response.status_code == 200
        assert len(response.get_json()["items"]) == 6


class TestLearningContentCoverage:
    """Every supported language must provide complete learning content."""

    def test_tutorial_available_in_all_languages(self):
        for lang in LANGUAGE_INFO:
            steps = get_tutorial(lang)
            assert len(steps) == 5, f"tutorial incomplete for {lang}"
            for step in steps:
                assert step["title"], f"missing title in {lang}"
                assert step["body"], f"missing body in {lang}"

    def test_markdown_help_available_in_all_languages(self):
        for lang in LANGUAGE_INFO:
            items = get_markdown_help(lang)
            assert len(items) == 6, f"help incomplete for {lang}"
            for item in items:
                assert item["label"], f"missing label in {lang}"
                assert item["hint"], f"missing hint in {lang}"

    def test_syntax_is_language_neutral(self):
        """Markdown syntax/example should be identical across languages."""
        en = get_markdown_help("en")
        it = get_markdown_help("it")
        for a, b in zip(en, it):
            assert a["syntax"] == b["syntax"]
            assert a["example"] == b["example"]
