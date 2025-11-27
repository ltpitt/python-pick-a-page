"""
HTML/CSS/JS generator.

Generates playable HTML files from parsed story data.
"""

import re
from pathlib import Path
from typing import Optional
import mistune
from .compiler import Story
from .templates import HTML_TEMPLATE, CSS_TEMPLATE, JAVASCRIPT_TEMPLATE
from .i18n import get_language


class HTMLGenerator:
    """Generates HTML output from parsed story data."""
    
    def generate(self, story: Story, base_path: Optional[Path] = None) -> str:
        """
        Generate complete HTML document from story data.
        
        Args:
            story: Parsed Story object
            base_path: Base path for resolving image files (optional)
            
        Returns:
            Complete HTML string with embedded CSS and JavaScript
        """
        if base_path is None:
            base_path = Path.cwd()
            
        # Generate HTML content for all sections
        sections_html = self._generate_sections(story, base_path)
        
        # Generate the story data JavaScript object
        story_data_js = self._generate_story_data(story)
        
        # Get current language for HTML lang attribute
        lang = get_language()
        
        # Combine everything
        html = HTML_TEMPLATE.format(
            lang=lang,
            title=story.metadata.title,
            css=CSS_TEMPLATE,
            content=sections_html,
            javascript=story_data_js + "\n" + JAVASCRIPT_TEMPLATE
        )
        
        return html
    
    def _generate_sections(self, story: Story, base_path: Path) -> str:
        """Generate HTML for all sections."""
        sections_html = []
        
        for i, section in enumerate(story.sections):
            # First section is visible, others hidden initially
            visibility = "block" if section.name == story.metadata.start_section else "none"
            
            section_html = f'<div class="section" id="section-{section.name}" data-section-name="{section.name}" style="display: {visibility};">\n'
            
            # Convert markdown content to HTML
            content_html = self._convert_markdown(section.content)
            
            # Process images
            content_html = self._process_images(content_html, base_path)
            
            section_html += content_html + '\n'
            
            # Generate choice buttons
            if section.choices:
                section_html += '<div class="choices">\n'
                for choice in section.choices:
                    section_html += f'  <button class="choice" data-target="{choice.target}">{choice.text}</button>\n'
                section_html += '</div>\n'
            
            section_html += '</div>\n\n'
            sections_html.append(section_html)
        
        return "\n".join(sections_html)
    
    def _convert_markdown(self, text: str) -> str:
        """Convert Markdown to HTML using mistune with GFM support.
        
        Supports:
        - Headers (# H1 through ###### H6)
        - Bold (**text** or __text__)
        - Italic (*text* or _text_)
        - Strikethrough (~~text~~)
        - Lists (- or * for unordered, 1. for ordered)
        - Blockquotes (> text)
        - Inline code (`code`)
        - Horizontal rules (---)
        - Links ([text](url))
        - Paragraphs (double newline)
        """
        # Remove choice syntax [[text]] or [[text|target]] before processing
        # This is our custom story navigation syntax
        text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', '', text)
        
        # Create mistune markdown parser with GitHub Flavored Markdown features
        # strikethrough=True enables ~~text~~ syntax
        markdown_parser = mistune.create_markdown(
            escape=False,  # Don't escape HTML (we control the input)
            plugins=['strikethrough', 'table', 'url']  # GFM features
        )
        
        # Convert markdown to HTML
        html = markdown_parser(text)
        
        # Mistune wraps everything in <p> tags, which is what we want
        return html.strip()
    
    def _process_images(self, html: str, base_path: Path) -> str:
        """Process image markdown and convert to HTML img tags with physical file paths."""
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Simply create an img tag with the physical file path
            # This keeps the HTML lightweight and lets the browser handle loading
            return f'<img src="{image_path}" alt="{alt_text}" />'
        
        # Replace markdown images with HTML img tags
        html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', replace_image, html)
        
        return html
    
    def _generate_story_data(self, story: Story) -> str:
        """Generate JavaScript object with story data."""
        js = "// Story data\n"
        js += "const storyData = {\n"
        js += f"  currentSection: '{story.metadata.start_section}',\n"
        js += f"  startSection: '{story.metadata.start_section}',\n"
        js += "  history: [],\n"
        js += "};\n"
        return js


def generate_html(story_data: dict) -> str:
    """
    Legacy function for backwards compatibility.
    
    Args:
        story_data: Parsed story data structure
        
    Returns:
        Complete HTML string with embedded CSS and JavaScript
    """
    # This is a backwards-compatible wrapper
    # New code should use HTMLGenerator().generate(story)
    raise NotImplementedError("Use HTMLGenerator().generate(story) instead")
