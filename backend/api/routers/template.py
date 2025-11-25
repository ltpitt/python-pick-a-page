"""
Template/Init Router - Story template generation and initialization.

Provides endpoints for:
- GET /api/template - Get story template with customization
- POST /api/new - Create new story from template
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from pathlib import Path
from typing import Optional

from backend.core.i18n import _, set_language, get_language_codes
from backend.utils import sanitize_filename

router = APIRouter(prefix="/api", tags=["templates"])

# Default stories directory
STORIES_DIR = Path("stories")
STORIES_DIR.mkdir(exist_ok=True)

class NewStoryRequest(BaseModel):
    """Request model for creating new story."""
    filename: str
    title: Optional[str] = None
    author: Optional[str] = None
    lang: Optional[str] = "en"

def get_story_template(title: str = "My Adventure", author: str = "Young Author", lang: str = "en") -> str:
    """
    Generate story template with customizable fields.
    
    Args:
        title: Story title
        author: Story author
        lang: Language code for localization
        
    Returns:
        Story template string
    """
    # Set language for translations
    if lang in get_language_codes():
        set_language(lang)
    
    template = f"""---
title: {title}
author: {author}
---

[[start]]

{_('template_welcome')}

{_('template_beginning')}

[[{_('template_continue')}]]

---

[[{_('template_continue')}]]

{_('template_body')}

{_('template_add_images')}

{_('template_choices')}

{_('template_end')}
"""
    
    return template

@router.get("/template")
async def get_template(
    title: str = Query("My Adventure", description="Story title"),
    author: str = Query("Young Author", description="Story author"),
    lang: str = Query("en", description="Language code")
):
    """
    Get story template with customization.
    
    Query Parameters:
    - title: Custom title for the story
    - author: Custom author name
    - lang: Language code (en, nl, it, etc.)
    
    Returns:
    - template: Story template string
    """
    template = get_story_template(title=title, author=author, lang=lang)
    
    return {
        "template": template,
        "title": title,
        "author": author,
        "lang": lang
    }

@router.post("/new")
async def create_new_story(request: NewStoryRequest):
    """
    Create new story file from template.
    
    Request Body:
    - filename: Filename for the new story
    - title: Optional custom title
    - author: Optional custom author
    - lang: Optional language code
    
    Returns:
    - success: Boolean indicating success
    - filename: Sanitized filename
    - message: Success message
    """
    try:
        # Sanitize filename
        filename = sanitize_filename(request.filename)
        
        # Use provided values or defaults
        title = request.title or filename.replace('.txt', '').replace('_', ' ').replace('-', ' ').title()
        author = request.author or _('template_author')
        lang = request.lang or 'en'
        
        # Generate template
        template = get_story_template(title=title, author=author, lang=lang)
        
        # Save to stories directory
        story_path = STORIES_DIR / filename
        story_path.write_text(template, encoding='utf-8')
        
        return {
            "success": True,
            "filename": filename,
            "message": f"Story created: {filename}",
            "path": str(story_path)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
