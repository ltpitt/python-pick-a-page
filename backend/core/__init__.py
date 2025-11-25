"""Core modules for pick_a_page backend.

Moved from the POC pick_a_page package to integrate with FastAPI backend.
"""

from .compiler import StoryCompiler, Story, Section, Choice, Image, ValidationError, StoryMetadata
from .generator import HTMLGenerator
from .i18n import TRANSLATIONS, get_available_languages, set_language, _
from .templates import HTML_TEMPLATE, CSS_TEMPLATE, JAVASCRIPT_TEMPLATE

__all__ = [
    'StoryCompiler',
    'Story',
    'Section',
    'Choice',
    'Image',
    'ValidationError',
    'StoryMetadata',
    'HTMLGenerator',
    'TRANSLATIONS',
    'get_available_languages',
    'set_language',
    '_',
    'HTML_TEMPLATE',
    'CSS_TEMPLATE',
    'JAVASCRIPT_TEMPLATE',
]
