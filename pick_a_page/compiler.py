"""
Story compiler module.

Parses story text files and converts them into structured data
that can be used to generate HTML output.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional


class ValidationError(Exception):
    """Raised when story validation fails."""
    pass


@dataclass
class StoryMetadata:
    """Metadata about the story."""
    title: str
    author: Optional[str] = None
    start_section: Optional[str] = None


@dataclass
class Choice:
    """A choice/link within a section."""
    text: str
    target: str  # Normalized section name


@dataclass
class Image:
    """An image reference within a section."""
    alt_text: str
    path: str


@dataclass
class Section:
    """A section of the story."""
    name: str  # Normalized name
    content: str
    choices: List[Choice] = field(default_factory=list)
    images: List[Image] = field(default_factory=list)


@dataclass
class Story:
    """Complete story structure."""
    metadata: StoryMetadata
    sections: List[Section]


class StoryCompiler:
    """Compiles story text into structured data."""

    def parse(self, content: str) -> Story:
        """
        Parse story content into structured format.
        
        Args:
            content: Raw story text
            
        Returns:
            Parsed Story object
            
        Raises:
            ValidationError: If story format is invalid
        """
        if not content or not content.strip():
            raise ValidationError("Story content is empty")
        
        # Extract metadata
        metadata = self._parse_metadata(content)
        
        # Split into sections
        sections = self._parse_sections(content)
        
        if not sections:
            raise ValidationError("No sections found in story")
        
        # Set default start section if not specified
        if not metadata.start_section:
            metadata.start_section = sections[0].name
        
        return Story(metadata=metadata, sections=sections)

    def _parse_metadata(self, content: str) -> StoryMetadata:
        """Extract metadata from the story header."""
        # Match metadata block: ---\n...metadata...\n---
        metadata_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        
        if not metadata_match:
            raise ValidationError("No metadata block found. Story must start with ---\\nmetadata\\n---")
        
        metadata_text = metadata_match.group(1)
        metadata_dict = {}
        
        for line in metadata_text.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                metadata_dict[key.strip()] = value.strip()
        
        if 'title' not in metadata_dict:
            raise ValidationError("Metadata must include 'title' field")
        
        return StoryMetadata(
            title=metadata_dict['title'],
            author=metadata_dict.get('author'),
            start_section=metadata_dict.get('start')
        )

    def _parse_sections(self, content: str) -> List[Section]:
        """Parse all sections from the story."""
        # Remove metadata block
        content_without_metadata = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, count=1, flags=re.DOTALL)
        
        # Split by section separators (---), but keep the content
        raw_sections = re.split(r'\n---\s*\n', content_without_metadata)
        
        sections = []
        seen_names = set()
        
        for raw_section in raw_sections:
            raw_section = raw_section.strip()
            if not raw_section:
                continue
            
            section = self._parse_section(raw_section)
            
            # Check for duplicates
            if section.name in seen_names:
                raise ValidationError(f"Duplicate section name (duplicate): {section.name}")
            
            seen_names.add(section.name)
            sections.append(section)
        
        return sections

    def _parse_section(self, raw_section: str) -> Section:
        """Parse a single section."""
        lines = raw_section.split('\n')
        
        # First line should be section header [[name]]
        header_line = lines[0].strip()
        header_match = re.match(r'^\[\[([^\]]+)\]\]$', header_line)
        
        if not header_match:
            raise ValidationError(f"Invalid section header: {header_line}. Expected [[section name]]")
        
        section_name = header_match.group(1)
        normalized_name = self._normalize_section_name(section_name)
        
        # Rest is content
        content = '\n'.join(lines[1:]).strip()
        
        # Extract choices
        choices = self._extract_choices(content)
        
        # Extract images
        images = self._extract_images(content)
        
        return Section(
            name=normalized_name,
            content=content,
            choices=choices,
            images=images
        )

    def _normalize_section_name(self, name: str) -> str:
        """Normalize section name to lowercase with hyphens."""
        # Convert to lowercase and replace spaces/underscores with hyphens
        normalized = name.lower()
        normalized = re.sub(r'[\s_]+', '-', normalized)
        # Remove any non-alphanumeric characters except hyphens
        normalized = re.sub(r'[^a-z0-9-]', '', normalized)
        return normalized

    def _extract_choices(self, content: str) -> List[Choice]:
        """Extract choices from section content."""
        choices = []
        
        # Match [[text]] or [[text|target]]
        choice_pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
        
        for match in re.finditer(choice_pattern, content):
            text = match.group(1).strip()
            target = match.group(2).strip() if match.group(2) else None
            
            # If no custom target, normalize the text as the target
            if not target:
                target = self._normalize_section_name(text)
            else:
                target = self._normalize_section_name(target)
            
            choices.append(Choice(text=text, target=target))
        
        return choices

    def _extract_images(self, content: str) -> List[Image]:
        """Extract image references from section content."""
        images = []
        
        # Match ![alt text](path)
        image_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        
        for match in re.finditer(image_pattern, content):
            alt_text = match.group(1).strip()
            path = match.group(2).strip()
            images.append(Image(alt_text=alt_text, path=path))
        
        return images

    def validate(self, story: Story) -> List[str]:
        """
        Validate story structure and return list of errors.
        
        Args:
            story: Story to validate
            
        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        
        # Build set of all section names
        section_names = {section.name for section in story.sections}
        
        # Check that start section exists
        if story.metadata.start_section and story.metadata.start_section not in section_names:
            errors.append(f"Start section '{story.metadata.start_section}' does not exist")
        
        # Track which sections are reachable
        reachable = set()
        if story.metadata.start_section:
            self._mark_reachable(story.metadata.start_section, story.sections, reachable)
        
        # Check all choices point to valid sections
        for section in story.sections:
            for choice in section.choices:
                if choice.target not in section_names:
                    errors.append(
                        f"Section '{section.name}' has choice pointing to "
                        f"non-existent section '{choice.target}'"
                    )
                else:
                    # Mark target as reachable
                    reachable.add(choice.target)
        
        # Check for orphaned sections (except start section)
        for section in story.sections:
            if section.name != story.metadata.start_section and section.name not in reachable:
                errors.append(f"Section '{section.name}' is unreachable (orphaned)")
        
        return errors

    def _mark_reachable(self, section_name: str, sections: List[Section], reachable: set):
        """Recursively mark sections as reachable."""
        if section_name in reachable:
            return  # Already visited
        
        reachable.add(section_name)
        
        # Find this section
        section = next((s for s in sections if s.name == section_name), None)
        if not section:
            return
        
        # Mark all targets as reachable
        for choice in section.choices:
            self._mark_reachable(choice.target, sections, reachable)
