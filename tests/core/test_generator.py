"""
Tests for the HTML generator module.

Following TDD approach: These tests are written FIRST (RED phase).
The generator.py implementation will be written to make these tests pass (GREEN phase).
"""

import pytest
import re
from pathlib import Path
from backend.core.compiler import StoryCompiler
from backend.core.generator import HTMLGenerator


class TestBasicGeneration:
    """Test basic HTML generation."""

    def test_generate_simple_html(self):
        """Should generate valid HTML5 document."""
        content = """---
title: Test Story
---

[[start]]

Hello world!"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Check HTML5 doctype
        assert html.strip().startswith("<!DOCTYPE html>")
        assert "<html" in html
        assert "</html>" in html
        
    def test_include_story_title(self):
        """Should include story title in HTML."""
        content = """---
title: My Amazing Story
---

[[start]]

Content"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        assert "My Amazing Story" in html
        assert "<title>My Amazing Story</title>" in html

    def test_include_meta_viewport(self):
        """Should include viewport meta tag for mobile."""
        content = """---
title: Test
---

[[start]]
Content"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        assert '<meta name="viewport"' in html


class TestContentGeneration:
    """Test generation of story content."""

    def test_include_section_content(self):
        """Should include section content in HTML."""
        content = """---
title: Test
---

[[start]]

This is the story content.
It has multiple lines."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        assert "This is the story content" in html

    def test_convert_markdown_bold(self):
        """Should convert **bold** markdown to HTML."""
        content = """---
title: Test
---

[[start]]

This is **very important** text."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Should convert to <strong> or <b> tags
        assert "<strong>very important</strong>" in html or "<b>very important</b>" in html

    def test_convert_markdown_italic(self):
        """Should convert *italic* markdown to HTML."""
        content = """---
title: Test
---

[[start]]

This is *emphasized* text."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Should convert to <em> or <i> tags
        assert "<em>emphasized</em>" in html or "<i>emphasized</i>" in html

    def test_preserve_paragraphs(self):
        """Should convert paragraph breaks to <p> tags."""
        content = """---
title: Test
---

[[start]]

First paragraph.

Second paragraph."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Should have multiple <p> tags
        assert html.count("<p>") >= 2


class TestChoiceGeneration:
    """Test generation of interactive choices."""

    def test_generate_choice_buttons(self):
        """Should generate buttons for choices."""
        content = """---
title: Test
---

[[start]]

Choose:

[[Go left]]
[[Go right]]"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Should have buttons or links with choice text
        assert "Go left" in html
        assert "Go right" in html

    def test_choice_buttons_have_targets(self):
        """Should include data attributes or links to target sections."""
        content = """---
title: Test
---

[[start]]

[[Go to end|ending]]

---

[[ending]]

The end."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Should reference the 'ending' section
        assert "ending" in html.lower()


class TestImageGeneration:
    """Test generation of images."""

    def test_include_image_tag(self):
        """Should generate <img> tags for images."""
        content = """---
title: Test
---

[[start]]

![A sunset](images/sunset.jpg)"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        assert "<img" in html
        assert 'alt="A sunset"' in html

    def test_embed_images_as_base64(self):
        """Should use physical file paths for images, not base64 encoding."""
        content = """---
title: Test
---

[[start]]

![Test image](tests/fixtures/images/test.jpg)"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story, base_path=Path.cwd())
        
        # Should have physical file path, NOT base64
        assert '<img src="tests/fixtures/images/test.jpg"' in html
        assert 'alt="Test image"' in html
        assert "data:image" not in html
        assert "base64" not in html


class TestStyleGeneration:
    """Test CSS style generation."""

    def test_include_css_styles(self):
        """Should include CSS styles in <style> tag."""
        content = """---
title: Test
---

[[start]]

Content"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        assert "<style>" in html
        assert "</style>" in html

    def test_include_print_styles(self):
        """Should include @media print styles for printing."""
        content = """---
title: Test
---

[[start]]

Content"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        assert "@media print" in html

    def test_button_styles_present(self):
        """Should include styles for choice buttons."""
        content = """---
title: Test
---

[[start]]

[[Choice]]"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Should have button/choice styles
        assert ".choice" in html or "button" in html


class TestJavaScriptGeneration:
    """Test JavaScript generation for interactivity."""

    def test_include_javascript(self):
        """Should include JavaScript in <script> tag."""
        content = """---
title: Test
---

[[start]]

[[Choice]]"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        assert "<script>" in html
        assert "</script>" in html

    def test_include_navigation_logic(self):
        """Should include JavaScript for navigating between sections."""
        content = """---
title: Test
---

[[start]]

[[Next|middle]]

---

[[middle]]

Content"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Should have some navigation-related JavaScript
        # (specific implementation will vary, but should have functions/listeners)
        script_section = html[html.find("<script>"):html.find("</script>")]
        assert len(script_section) > 50  # Has actual code, not just empty tags


class TestCompleteStory:
    """Test generation of complete, multi-section stories."""

    def test_generate_from_fixture(self):
        """Should generate complete HTML from valid story fixture."""
        with open(Path(__file__).parent.parent / "fixtures" / "valid_story.txt") as f:
            content = f.read()
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Check all sections are present
        assert "My First Adventure" in html
        assert "mysterious forest" in html
        assert "Explore the forest" in html
        assert "Follow the path" in html

    def test_output_is_valid_html5(self):
        """Generated HTML should be valid HTML5."""
        content = """---
title: Complete Story
author: Test
---

[[start]]

Welcome! This is a **bold** statement.

![Image](test.jpg)

[[Next]]

---

[[Next]]

The end."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        # Basic HTML5 validation checks
        assert html.strip().startswith("<!DOCTYPE html>")
        assert "<html" in html
        assert "<head>" in html
        assert "</head>" in html
        assert "<body>" in html
        assert "</body>" in html
        assert "</html>" in html
        
        # All opening tags have closing tags
        assert html.count("<style>") == html.count("</style>")
        assert html.count("<script>") == html.count("</script>")
        assert html.count("<div") == html.count("</div>")
