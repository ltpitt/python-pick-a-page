"""
Integration tests for complete story compilation and navigation.

Tests the full workflow from parsing to HTML generation to verifying
all possible story paths work correctly.
"""

import pytest
import re
from pathlib import Path
from backend.core.compiler import StoryCompiler
from backend.core.generator import HTMLGenerator


class TestValidStoryAllPaths:
    """Test all possible paths through the valid_story.txt fixture."""
    
    @pytest.fixture
    def story_html(self):
        """Generate HTML from the valid story fixture."""
        with open(Path(__file__).parent.parent / "fixtures" / "valid_story.txt") as f:
            content = f.read()
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        # Validate first
        errors = compiler.validate(story)
        assert len(errors) == 0, f"Story has validation errors: {errors}"
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        return html, story
    
    def test_story_structure(self, story_html):
        """Verify the story has the expected structure."""
        html, story = story_html
        
        # Check we have all 4 sections
        assert len(story.sections) == 4
        
        section_names = [s.name for s in story.sections]
        assert "beginning" in section_names
        assert "explore-the-forest" in section_names
        assert "follow-the-path" in section_names
        assert "follow-the-stream" in section_names
        
    def test_path_1_explore_then_stream(self, story_html):
        """Test path: beginning → explore forest → follow stream (treasure)."""
        html, story = story_html
        
        # Verify beginning section exists and has both choices
        beginning = next(s for s in story.sections if s.name == "beginning")
        assert len(beginning.choices) == 2
        assert any(c.target == "explore-the-forest" for c in beginning.choices)
        assert any(c.target == "follow-the-path" for c in beginning.choices)
        
        # Verify explore forest section
        explore = next(s for s in story.sections if s.name == "explore-the-forest")
        assert len(explore.choices) == 2
        assert any(c.target == "follow-the-stream" for c in explore.choices)
        assert any(c.target == "beginning" for c in explore.choices)  # Go back
        
        # Verify follow stream section (ending)
        stream = next(s for s in story.sections if s.name == "follow-the-stream")
        assert len(stream.choices) == 0  # No choices = ending
        assert "treasure" in stream.content.lower()
        
    def test_path_2_follow_path(self, story_html):
        """Test path: beginning → follow path (cottage ending)."""
        html, story = story_html
        
        # Verify beginning has follow-the-path choice
        beginning = next(s for s in story.sections if s.name == "beginning")
        assert any(c.target == "follow-the-path" for c in beginning.choices)
        
        # Verify follow path section (ending)
        path = next(s for s in story.sections if s.name == "follow-the-path")
        assert len(path.choices) == 0  # No choices = ending
        assert "cottage" in path.content.lower()
        
    def test_path_3_explore_then_back(self, story_html):
        """Test path: beginning → explore → go back → follow path."""
        html, story = story_html
        
        # This tests the "go back" functionality
        explore = next(s for s in story.sections if s.name == "explore-the-forest")
        
        # Verify "go back" choice exists
        go_back_choice = next((c for c in explore.choices if c.target == "beginning"), None)
        assert go_back_choice is not None, "No 'go back' choice found in explore section"
        assert go_back_choice.text == "Go back"
        
        # Verify that going back leads to beginning which has follow-the-path
        beginning = next(s for s in story.sections if s.name == "beginning")
        assert any(c.target == "follow-the-path" for c in beginning.choices)
        
    def test_all_sections_reachable(self, story_html):
        """Verify all sections can be reached from the start."""
        html, story = story_html
        
        # Track reachability
        reachable = set()
        to_visit = ["beginning"]  # Start section
        
        while to_visit:
            current = to_visit.pop()
            if current in reachable:
                continue
            reachable.add(current)
            
            # Find section
            section = next((s for s in story.sections if s.name == current), None)
            if section:
                for choice in section.choices:
                    if choice.target not in reachable:
                        to_visit.append(choice.target)
        
        # All sections should be reachable
        all_section_names = {s.name for s in story.sections}
        assert reachable == all_section_names, f"Unreachable sections: {all_section_names - reachable}"
        
    def test_no_dead_ends_with_choices(self, story_html):
        """Verify no section has choices that all lead to nowhere."""
        html, story = story_html
        
        for section in story.sections:
            if section.choices:
                # At least one choice should lead somewhere
                for choice in section.choices:
                    target_exists = any(s.name == choice.target for s in story.sections)
                    assert target_exists, f"Section '{section.name}' has choice to non-existent '{choice.target}'"
    
    def test_endings_have_no_choices(self, story_html):
        """Verify that ending sections have no choices."""
        html, story = story_html
        
        # These are known endings
        expected_endings = ["follow-the-path", "follow-the-stream"]
        
        for ending_name in expected_endings:
            section = next((s for s in story.sections if s.name == ending_name), None)
            assert section is not None, f"Ending section '{ending_name}' not found"
            assert len(section.choices) == 0, f"Ending section '{ending_name}' should have no choices"


class TestHTMLNavigationStructure:
    """Test the generated HTML navigation structure."""
    
    @pytest.fixture
    def story_html(self):
        """Generate HTML from the valid story fixture."""
        with open(Path(__file__).parent.parent / "fixtures" / "valid_story.txt") as f:
            content = f.read()
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        return html
    
    def test_all_sections_in_html(self, story_html):
        """Verify all sections appear in the HTML."""
        html = story_html
        
        assert 'id="section-beginning"' in html
        assert 'id="section-explore-the-forest"' in html
        assert 'id="section-follow-the-path"' in html
        assert 'id="section-follow-the-stream"' in html
        
    def test_all_buttons_have_targets(self, story_html):
        """Verify all buttons have data-target attributes."""
        html = story_html
        
        # Find all choice buttons
        button_pattern = r'<button class="choice" data-target="([^"]+)">([^<]+)</button>'
        buttons = re.findall(button_pattern, html)
        
        # Should have at least 4 buttons (2 in beginning, 2 in explore)
        assert len(buttons) >= 4, f"Expected at least 4 buttons, found {len(buttons)}"
        
        # All buttons should have targets
        for target, text in buttons:
            assert target, f"Button '{text}' has no target"
            
    def test_javascript_navigation_present(self, story_html):
        """Verify navigation JavaScript is included."""
        html = story_html
        
        assert "handleChoiceClick" in html
        assert "navigateToSection" in html
        assert "addEventListener" in html
        assert "data-target" in html
        
    def test_event_delegation_setup(self, story_html):
        """Verify event delegation is used (not individual handlers)."""
        html = story_html
        
        # Should use delegation on #story container
        assert 'document.getElementById(\'story\').addEventListener' in html
        # Should NOT attach individual handlers in a loop
        assert 'forEach(button =>' not in html or 'attachChoiceHandlers' not in html


class TestStoryPathsEndToEnd:
    """End-to-end tests simulating user navigation."""
    
    @pytest.fixture
    def parsed_story(self):
        """Load and parse the valid story."""
        with open(Path(__file__).parent.parent / "fixtures" / "valid_story.txt") as f:
            content = f.read()
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        return story
    
    def simulate_path(self, story, path):
        """
        Simulate following a path through the story.
        
        Args:
            story: Parsed story object
            path: List of section names to visit
            
        Returns:
            List of sections visited
        """
        visited = []
        current = path[0]
        
        for next_section in path[1:]:
            # Find current section
            section = next((s for s in story.sections if s.name == current), None)
            assert section is not None, f"Section '{current}' not found"
            visited.append(section)
            
            # Verify we can reach next section
            has_choice = any(c.target == next_section for c in section.choices)
            assert has_choice, f"Cannot navigate from '{current}' to '{next_section}'"
            
            current = next_section
        
        # Add final section
        final = next((s for s in story.sections if s.name == current), None)
        if final:
            visited.append(final)
        
        return visited
    
    def test_treasure_ending_path(self, parsed_story):
        """Simulate: beginning → explore → stream → treasure!"""
        path = ["beginning", "explore-the-forest", "follow-the-stream"]
        visited = self.simulate_path(parsed_story, path)
        
        assert len(visited) == 3
        assert visited[-1].name == "follow-the-stream"
        assert "treasure" in visited[-1].content.lower()
        
    def test_cottage_ending_path(self, parsed_story):
        """Simulate: beginning → path → cottage!"""
        path = ["beginning", "follow-the-path"]
        visited = self.simulate_path(parsed_story, path)
        
        assert len(visited) == 2
        assert visited[-1].name == "follow-the-path"
        assert "cottage" in visited[-1].content.lower()
        
    def test_backtrack_path(self, parsed_story):
        """Simulate: beginning → explore → back to beginning → path → cottage!"""
        path = ["beginning", "explore-the-forest", "beginning", "follow-the-path"]
        visited = self.simulate_path(parsed_story, path)
        
        assert len(visited) == 4
        # Verify we went to beginning twice
        assert visited[0].name == "beginning"
        assert visited[2].name == "beginning"
        # Verify we ended at cottage
        assert visited[-1].name == "follow-the-path"


class TestStoryValidation:
    """Test story validation catches common issues."""
    
    def test_valid_story_passes_validation(self):
        """The valid_story.txt should pass all validation."""
        with open(Path(__file__).parent.parent / "fixtures" / "valid_story.txt") as f:
            content = f.read()
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        errors = compiler.validate(story)
        
        assert len(errors) == 0, f"Valid story failed validation: {errors}"
        
    def test_all_links_point_to_existing_sections(self):
        """Verify no broken links in valid story."""
        with open(Path(__file__).parent.parent / "fixtures" / "valid_story.txt") as f:
            content = f.read()
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        section_names = {s.name for s in story.sections}
        
        for section in story.sections:
            for choice in section.choices:
                assert choice.target in section_names, \
                    f"Section '{section.name}' links to non-existent '{choice.target}'"


class TestNarrationContent:
    """Test that story narration text is correctly preserved in HTML."""
    
    @pytest.fixture
    def story_and_html(self):
        """Load story and generate HTML."""
        with open(Path(__file__).parent.parent / "fixtures" / "valid_story.txt") as f:
            content = f.read()
        
        compiler = StoryCompiler()
        story = compiler.parse(content)
        
        generator = HTMLGenerator()
        html = generator.generate(story)
        
        return story, html
    
    def test_beginning_narration_in_html(self, story_and_html):
        """Verify beginning section narration appears correctly in HTML."""
        story, html = story_and_html
        
        beginning = next(s for s in story.sections if s.name == "beginning")
        
        # Check key phrases from the narration
        assert "mysterious forest" in html
        assert "sun is shining" in html
        assert "What do you want to do?" in html
        
        # Verify the content is in the right section
        assert 'id="section-beginning"' in html
        section_start = html.find('id="section-beginning"')
        section_end = html.find('</div>', section_start)
        section_html = html[section_start:section_end]
        
        assert "mysterious forest" in section_html
        
    def test_explore_narration_preserved(self, story_and_html):
        """Verify explore forest narration is correct."""
        story, html = story_and_html
        
        explore = next(s for s in story.sections if s.name == "explore-the-forest")
        
        # Check the actual narration content
        assert "venture deeper into the forest" in html.lower()
        assert "sparkling stream" in html.lower()
        
    def test_all_section_content_present(self, story_and_html):
        """Verify ALL section narrations appear in the HTML."""
        story, html = story_and_html
        
        for section in story.sections:
            # Get first significant word from content (not markdown)
            content_text = section.content.replace("*", "").replace("[[", "").strip()
            first_words = content_text.split()[:3]
            
            # At least some of the content should be in HTML
            if first_words:
                first_phrase = " ".join(first_words[:2])
                assert first_phrase.lower() in html.lower(), \
                    f"Section '{section.name}' content not found in HTML. Looking for: {first_phrase}"
    
    def test_choice_buttons_contain_text(self, story_and_html):
        """Verify choice button text matches the story."""
        story, html = story_and_html
        
        for section in story.sections:
            for choice in section.choices:
                # The choice text should appear in a button
                button_pattern = f'<button[^>]*>{re.escape(choice.text)}</button>'
                assert re.search(button_pattern, html), \
                    f"Choice text '{choice.text}' not found in HTML buttons"
    
    def test_section_content_not_duplicated_in_template(self, story_and_html):
        """
        Verify section content appears exactly once in the initial HTML
        (not counting clones that happen during navigation).
        """
        story, html = story_and_html
        
        # Each section should appear once with its ID
        for section in story.sections:
            section_id = f'id="section-{section.name}"'
            count = html.count(section_id)
            assert count == 1, \
                f"Section '{section.name}' appears {count} times in HTML (should be 1)"
    
    def test_cloned_sections_preserve_content(self, story_and_html):
        """
        Test that when sections are cloned (via JavaScript), the content
        is preserved. This tests the HTML structure allows cloning.
        """
        story, html = story_and_html
        
        # Find a section that can be revisited (beginning has "go back" pointing to it)
        beginning = next(s for s in story.sections if s.name == "beginning")
        
        # Extract the beginning section HTML
        section_pattern = r'<div class="section" id="section-beginning"[^>]*>(.*?)</div>\s*(?:<div|</div>|<script)'
        match = re.search(section_pattern, html, re.DOTALL)
        
        assert match, "Could not find beginning section in HTML"
        
        section_html = match.group(1)
        
        # Verify the narration text is in the section
        assert "mysterious forest" in section_html.lower()
        assert "sun is shining" in section_html.lower()
        
        # Verify buttons are in the section
        assert 'data-target="explore-the-forest"' in section_html
        assert 'data-target="follow-the-path"' in section_html
        
    def test_markdown_formatting_preserved(self, story_and_html):
        """Verify markdown formatting (bold/italic) is converted to HTML."""
        story, html = story_and_html
        
        # If any section has bold/italic, it should be converted
        has_markdown = any("**" in s.content or "*" in s.content for s in story.sections)
        
        if has_markdown:
            # Should have HTML equivalents
            assert "<strong>" in html or "<b>" in html or \
                   "<em>" in html or "<i>" in html, \
                   "Markdown formatting not converted to HTML"
    
    def test_paragraph_breaks_maintained(self, story_and_html):
        """Verify paragraph breaks create proper <p> tags."""
        story, html = story_and_html
        
        # Should have multiple paragraph tags
        p_count = html.count("<p>")
        assert p_count >= 4, f"Expected at least 4 paragraphs, found {p_count}"
        
        # Each <p> should have closing </p>
        assert html.count("<p>") == html.count("</p>"), \
            "Mismatched paragraph tags"
