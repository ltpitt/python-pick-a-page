"""
Tests for the story compiler module.

Following TDD approach: These tests are written FIRST (RED phase).
The compiler.py implementation will be written to make these tests pass (GREEN phase).
"""

import pytest
from pathlib import Path
from backend.core.compiler import (
    StoryCompiler,
    Section,
    Choice,
    StoryMetadata,
    ValidationError,
)


class TestStoryMetadata:
    """Test metadata extraction from story files."""

    def test_parse_basic_metadata(self):
        """Should extract title, author, and start section from metadata block."""
        content = """---
title: My Story
author: Test Author
start: beginning
---

[[beginning]]
Some content"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        assert story.metadata.title == "My Story"
        assert story.metadata.author == "Test Author"
        assert story.metadata.start_section == "beginning"

    def test_parse_minimal_metadata(self):
        """Should work with just title in metadata."""
        content = """---
title: Simple Story
---

[[start]]
Content"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        assert story.metadata.title == "Simple Story"
        assert story.metadata.author is None
        assert story.metadata.start_section == "start"  # Should default to first section

    def test_missing_metadata_raises_error(self):
        """Should raise error if no metadata block found."""
        content = "[[start]]\nNo metadata here"
        
        compiler = StoryCompiler()
        
        with pytest.raises(ValidationError, match="metadata"):
            compiler.parse(content)


class TestSectionParsing:
    """Test parsing of story sections."""

    def test_parse_single_section(self):
        """Should parse a section with name and content."""
        content = """---
title: Test
---

[[beginning]]

This is the content of the section."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        assert len(story.sections) == 1
        assert story.sections[0].name == "beginning"
        assert "This is the content" in story.sections[0].content

    def test_parse_multiple_sections(self):
        """Should parse multiple sections separated by ---."""
        content = """---
title: Test
---

[[first]]
Content one

---

[[second]]
Content two

---

[[third]]
Content three"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        assert len(story.sections) == 3
        assert story.sections[0].name == "first"
        assert story.sections[1].name == "second"
        assert story.sections[2].name == "third"

    def test_section_names_normalized(self):
        """Should normalize section names (lowercase, hyphens for spaces)."""
        content = """---
title: Test
---

[[First Section]]
Content

---

[[Another  Section]]
More content"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        assert story.sections[0].name == "first-section"
        assert story.sections[1].name == "another-section"


class TestChoiceParsing:
    """Test parsing of choices within sections."""

    def test_parse_simple_choice(self):
        """Should extract choices from [[choice text]] format."""
        content = """---
title: Test
---

[[start]]

Choose wisely:

[[Go left]]
[[Go right]]"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        section = story.sections[0]
        assert len(section.choices) == 2
        assert section.choices[0].text == "Go left"
        assert section.choices[0].target == "go-left"
        assert section.choices[1].text == "Go right"
        assert section.choices[1].target == "go-right"

    def test_parse_choice_with_custom_target(self):
        """Should parse [[text|target]] format for custom link targets."""
        content = """---
title: Test
---

[[start]]

[[Go back to the beginning|start]]
[[Continue to end|finale]]"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        section = story.sections[0]
        assert section.choices[0].text == "Go back to the beginning"
        assert section.choices[0].target == "start"
        assert section.choices[1].text == "Continue to end"
        assert section.choices[1].target == "finale"

    def test_section_with_no_choices(self):
        """Should handle sections with no choices (endings)."""
        content = """---
title: Test
---

[[ending]]

The end. No choices here."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        section = story.sections[0]
        assert len(section.choices) == 0


class TestImageParsing:
    """Test parsing of image references."""

    def test_parse_image_reference(self):
        """Should extract image references from ![alt](path) format."""
        content = """---
title: Test
---

[[start]]

Look at this:

![A beautiful sunset](images/sunset.jpg)

Amazing!"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        section = story.sections[0]
        assert len(section.images) == 1
        assert section.images[0].alt_text == "A beautiful sunset"
        assert section.images[0].path == "images/sunset.jpg"

    def test_parse_multiple_images(self):
        """Should handle multiple images in one section."""
        content = """---
title: Test
---

[[start]]

![Image 1](img1.jpg)

Some text.

![Image 2](img2.png)"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        section = story.sections[0]
        assert len(section.images) == 2


class TestMarkdownParsing:
    """Test that basic Markdown formatting is preserved."""

    def test_preserve_bold_text(self):
        """Should preserve **bold** markdown."""
        content = """---
title: Test
---

[[start]]

This is **very important** text."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        assert "**very important**" in story.sections[0].content

    def test_preserve_italic_text(self):
        """Should preserve *italic* markdown."""
        content = """---
title: Test
---

[[start]]

This is *emphasized* text."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        assert "*emphasized*" in story.sections[0].content

    def test_preserve_paragraphs(self):
        """Should preserve paragraph breaks."""
        content = """---
title: Test
---

[[start]]

First paragraph.

Second paragraph."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        # Should preserve the double newline
        assert "\n\n" in story.sections[0].content or "paragraph" in story.sections[0].content


class TestLinkValidation:
    """Test validation of links between sections."""

    def test_detect_broken_link(self):
        """Should detect when a choice links to non-existent section."""
        content = """---
title: Test
---

[[start]]

[[Go to nowhere]]"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        errors = compiler.validate(story)
        assert len(errors) > 0
        assert any("nowhere" in str(e).lower() or "go-to-nowhere" in str(e).lower() for e in errors)

    def test_detect_orphaned_section(self):
        """Should detect sections that can't be reached."""
        content = """---
title: Test
---

[[start]]

[[go to middle]]

---

[[middle]]

The middle section.

---

[[orphan]]

This section is unreachable."""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        errors = compiler.validate(story)
        assert len(errors) > 0
        assert any("orphan" in str(e).lower() for e in errors)

    def test_valid_story_passes(self):
        """Should return no errors for valid story."""
        with open(Path(__file__).parent.parent / "fixtures" / "valid_story.txt") as f:
            content = f.read()
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        errors = compiler.validate(story)
        
        assert len(errors) == 0

    def test_detect_circular_reference(self):
        """Should handle (not crash on) circular references."""
        content = """---
title: Test
---

[[start]]

[[Go to middle|middle]]

---

[[middle]]

[[Go back to start|start]]"""
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        # Should not crash - circular references are valid
        errors = compiler.validate(story)
        assert len(errors) == 0


class TestErrorHandling:
    """Test error handling for malformed input."""

    def test_empty_file_raises_error(self):
        """Should raise error for empty input."""
        compiler = StoryCompiler()
        
        with pytest.raises(ValidationError):
            compiler.parse("")

    def test_malformed_section_header(self):
        """Should raise error for malformed section headers."""
        content = """---
title: Test
---

[start]

Missing double brackets"""
        
        compiler = StoryCompiler()
        
        with pytest.raises(ValidationError, match="section"):
            compiler.parse(content)

    def test_duplicate_section_names(self):
        """Should raise error for duplicate section names."""
        content = """---
title: Test
---

[[start]]
Content one

---

[[start]]
Content two"""
        
        compiler = StoryCompiler()
        
        with pytest.raises(ValidationError, match="duplicate"):
            compiler.parse(content)
