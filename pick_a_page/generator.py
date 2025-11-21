"""
HTML/CSS/JS generator.

Generates playable HTML files from parsed story data.
"""

import re
import base64
from pathlib import Path
from typing import Optional
from .compiler import Story, Section
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
        """Convert basic Markdown to HTML."""
        # Remove choice syntax [[text]] or [[text|target]]
        text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', '', text)
        
        # Convert **bold** to <strong>
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        
        # Convert *italic* to <em>
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        
        # Split into paragraphs and wrap in <p> tags
        paragraphs = text.strip().split('\n\n')
        html_paragraphs = [f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()]
        
        return '\n'.join(html_paragraphs)
    
    def _process_images(self, html: str, base_path: Path) -> str:
        """Process image markdown and embed as base64 if file exists."""
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Try to read and embed the image
            full_path = base_path / image_path
            if full_path.exists():
                try:
                    with open(full_path, 'rb') as f:
                        image_data = f.read()
                    
                    # Detect image type
                    if image_path.lower().endswith('.png'):
                        mime_type = 'image/png'
                    elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
                        mime_type = 'image/jpeg'
                    elif image_path.lower().endswith('.gif'):
                        mime_type = 'image/gif'
                    else:
                        mime_type = 'image/jpeg'  # default
                    
                    # Encode as base64
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                    return f'<img src="data:{mime_type};base64,{base64_data}" alt="{alt_text}" />'
                except Exception:
                    # If we can't read the file, use the path as-is
                    return f'<img src="{image_path}" alt="{alt_text}" />'
            else:
                # File doesn't exist, use path as-is
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
