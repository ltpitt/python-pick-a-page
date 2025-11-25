"""
Template/Init Router - Story template generation and initialization.

Provides endpoints for:
- GET /api/template - Get story template with customization
- POST /api/new - Create new story from template
"""

from flask import Blueprint, jsonify, request, abort
from pathlib import Path

from backend.core.i18n import _, set_language, get_language_codes
from backend.utils import sanitize_filename

bp = Blueprint('template', __name__)

# Default stories directory
STORIES_DIR = Path("stories")
STORIES_DIR.mkdir(exist_ok=True)


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


@bp.route("/template")
def get_template():
    """
    Get story template with customization.
    
    Query Parameters:
    - title: Custom title for the story
    - author: Custom author name
    - lang: Language code (en, nl, it, etc.)
    
    Returns:
    - template: Story template string
    """
    title = request.args.get('title', 'My Adventure')
    author = request.args.get('author', 'Young Author')
    lang = request.args.get('lang', 'en')
    
    template = get_story_template(title=title, author=author, lang=lang)
    
    return jsonify({
        "template": template,
        "title": title,
        "author": author,
        "lang": lang
    })


@bp.route("/new", methods=["POST"])
def create_new_story():
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
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")
    
    filename = data.get('filename')
    if not filename:
        abort(422, description="Filename is required")
    
    try:
        # Sanitize filename
        filename = sanitize_filename(filename)
        
        # Use provided values or defaults
        title = data.get('title') or filename.replace('.txt', '').replace('_', ' ').replace('-', ' ').title()
        author = data.get('author') or _('template_author')
        lang = data.get('lang') or 'en'
        
        # Generate template
        template = get_story_template(title=title, author=author, lang=lang)
        
        # Save to stories directory
        story_path = STORIES_DIR / filename
        story_path.write_text(template, encoding='utf-8')
        
        return jsonify({
            "success": True,
            "filename": filename,
            "message": f"Story created: {filename}",
            "path": str(story_path)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
