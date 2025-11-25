"""Story CRUD operations router.
"""

from pathlib import Path
from flask import Blueprint, jsonify, request, abort

from backend.core.compiler import StoryCompiler
from backend.utils import is_safe_path, sanitize_filename

bp = Blueprint('stories', __name__)

# Get stories directory from project root
STORIES_DIR = Path(__file__).parent.parent.parent.parent / "stories"
OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "output"


@bp.route("/stories")
def list_stories():
    """List all available stories with metadata."""
    stories = []
    
    if STORIES_DIR.exists():
        for story_file in STORIES_DIR.glob('*.txt'):
            try:
                with open(story_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                compiler = StoryCompiler()
                story = compiler.parse(content)
                stories.append({
                    'filename': story_file.name,
                    'title': story.metadata.title,
                    'author': story.metadata.author,
                    'sections': len(story.sections)
                })
            except Exception as e:
                stories.append({
                    'filename': story_file.name,
                    'title': story_file.stem.replace('_', ' ').title(),
                    'author': 'Unknown',
                    'error': str(e)
                })
    
    return jsonify(stories)


@bp.route("/story/<path:filename>")
def get_story_content(filename: str):
    """Get raw content of a story file."""
    is_safe, story_path = is_safe_path(STORIES_DIR, filename)
    if not is_safe:
        abort(403, description="Invalid file path")
    
    if not story_path.exists() or not story_path.is_file():
        abort(404, description=f"Story not found: {filename}")
    
    try:
        with open(story_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'content': content, 'filename': filename})
    except Exception as e:
        abort(500, description=f"Error reading story: {str(e)}")


@bp.route("/save", methods=["POST"])
def save_story():
    """Save story to file."""
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")
    
    content = data.get('content', '')
    filename = data.get('filename', '')
    
    if not filename:
        abort(400, description="No filename provided")
    
    filename = sanitize_filename(filename)
    
    is_safe, story_path = is_safe_path(STORIES_DIR, filename)
    if not is_safe:
        abort(403, description="Invalid filename")
    
    try:
        STORIES_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(story_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'message': f'Story saved as {filename}',
            'filename': filename
        })
    except Exception as e:
        abort(500, description=str(e))


@bp.route("/delete", methods=["POST"])
def delete_story():
    """Delete a story file."""
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")
    
    filename = data.get('filename', '')
    
    if not filename:
        abort(400, description='No filename provided')
    
    is_safe, story_path = is_safe_path(STORIES_DIR, filename)
    if not is_safe:
        abort(403, description="Invalid filename")
    
    if not story_path.exists():
        abort(404, description='Story not found')
    
    try:
        story_path.unlink()
        return jsonify({
            'success': True,
            'message': f'Story {filename} deleted'
        })
    except Exception as e:
        abort(500, description=str(e))
