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
from backend.core.learning import (
    get_tutorial,
    get_markdown_help,
    get_ui_labels,
    get_error_hint,
)


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

    def test_help_includes_badges_label(self, client):
        data = client.get("/api/help/markdown").get_json()
        assert data["badges"]

    def test_badges_label_localized_for_italian(self, client):
        en = client.get("/api/help/markdown?lang=en").get_json()["badges"]
        it = client.get("/api/help/markdown?lang=it").get_json()["badges"]
        assert en != it


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

    def test_ui_labels_available_in_all_languages(self):
        for lang in LANGUAGE_INFO:
            labels = get_ui_labels(lang)
            for key in ("tutorial_cta", "tutorial_heading", "tutorial_done",
                        "help_summary", "badges_label"):
                assert labels[key], f"missing {key} for {lang}"


# Story fragments that trigger each known validator/compiler message.
_HINT_CASES = {
    "broken_choice": "---\ntitle: T\n---\n\n[[start]]\nGo [[Nowhere]]\n",
    "orphaned": "---\ntitle: T\n---\n\n[[start]]\nHi\n\n---\n\n[[lonely]]\nAlone\n",
    "empty": "   ",
    "no_metadata": "[[start]]\nNo header here\n",
    "no_title": "---\nauthor: Me\n---\n\n[[start]]\nHi\n",
    "bad_header": "---\ntitle: T\n---\n\nnot a header\nHi\n",
}


class TestFriendlyHints:
    """The validator's technical messages become kid-friendly hints."""

    def test_broken_choice_message_maps_to_hint(self):
        msg = "Section 'start' has choice pointing to non-existent section 'cave'"
        hint = get_error_hint(msg, "en")
        assert hint is not None
        assert "cave" in hint

    def test_orphaned_message_maps_to_hint(self):
        hint = get_error_hint("Section 'lonely' is unreachable (orphaned)", "en")
        assert hint is not None
        assert "lonely" in hint

    def test_unknown_message_returns_none(self):
        assert get_error_hint("Something totally unexpected", "en") is None

    def test_hint_localized_for_italian(self):
        msg = "Section 'start' is unreachable (orphaned)"
        assert get_error_hint(msg, "en") != get_error_hint(msg, "it")

    def test_hint_unknown_language_falls_back_to_english(self):
        msg = "Section 'start' is unreachable (orphaned)"
        assert get_error_hint(msg, "xx") == get_error_hint(msg, "en")

    def test_all_known_messages_have_hints_in_every_language(self):
        messages = [
            "Section 'a' has choice pointing to non-existent section 'b'",
            "Section 'a' is unreachable (orphaned)",
            "Start section 'a' does not exist",
            "Story content is empty",
            "No metadata block found. Story must start with ...",
            "Metadata must include 'title' field",
            "No sections found in story",
            "Invalid section header: oops. Expected [[section name]]",
            "Duplicate section name (duplicate): a",
        ]
        for lang in LANGUAGE_INFO:
            for msg in messages:
                assert get_error_hint(msg, lang), f"no hint for '{msg}' in {lang}"


class TestValidateReturnsHints:
    """The /api/validate endpoint surfaces friendly hints in error_details."""

    def test_broken_link_validation_includes_hint(self, client):
        story = _HINT_CASES["broken_choice"]
        data = client.post("/api/validate", json={"content": story}).get_json()
        assert data["valid"] is False
        assert any(d.get("hint") for d in data["error_details"])

    def test_hints_are_localized(self, client):
        story = _HINT_CASES["broken_choice"]
        en = client.post("/api/validate", json={"content": story, "lang": "en"}).get_json()
        it = client.post("/api/validate", json={"content": story, "lang": "it"}).get_json()
        assert en["error_details"][0]["hint"] != it["error_details"][0]["hint"]

    def test_parse_error_also_gets_hint(self, client):
        story = _HINT_CASES["no_metadata"]
        data = client.post("/api/validate", json={"content": story}).get_json()
        assert data["valid"] is False
        assert data["error_details"][0]["hint"]

    def test_unknown_language_falls_back(self, client):
        story = _HINT_CASES["broken_choice"]
        data = client.post("/api/validate", json={"content": story, "lang": "zz"}).get_json()
        assert data["error_details"][0]["hint"]
