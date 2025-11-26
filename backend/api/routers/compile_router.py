"""Story compilation and validation router.
"""

import re
from pathlib import Path
from flask import Blueprint, jsonify, request, abort, send_file

from backend.core.compiler import StoryCompiler
from backend.core.generator import HTMLGenerator
from backend.utils import sanitize_filename

bp = Blueprint('compile', __name__)
play_bp = Blueprint('play', __name__)  # Separate blueprint for /play endpoint (mounted without /api prefix)

# Get output directory from project root
OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "output"


@bp.route("/compile", methods=["POST"])
def compile_story():
    """Compile story to HTML."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No JSON data provided'})
    
    content = data.get('content', '')
    filename = data.get('filename', '')
    
    try:
        # Sanitize filename and convert to HTML filename
        story_name = sanitize_filename(filename, extension='', default='story')
        story_name = story_name.replace('.txt', '')
        
        # Parse and validate
        compiler = StoryCompiler()
        story = compiler.parse(content)
        errors = compiler.validate(story)
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            })
        
        # Generate HTML (use stories/ as base path for image resolution)
        generator = HTMLGenerator()
        stories_dir = Path(__file__).parent.parent.parent.parent / "stories"
        html_content = generator.generate(story, base_path=stories_dir)
        
        # Save to output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        html_path = OUTPUT_DIR / f"{story_name}.html"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return jsonify({
            'success': True,
            'message': 'Story compiled successfully',
            'play_url': f'/play/{story_name}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@bp.route("/validate", methods=["POST"])
def validate_story():
    """Validate story structure."""
    data = request.get_json()
    if not data:
        return jsonify({
            'valid': False,
            'errors': ['No JSON data provided']
        })
    
    content = data.get('content', '')
    
    try:
        compiler = StoryCompiler()
        story = compiler.parse(content)
        errors = compiler.validate(story)
        
        return jsonify({
            'valid': len(errors) == 0,
            'errors': errors,
            'sections': len(story.sections),
            'title': story.metadata.title,
            'author': story.metadata.author
        })
    except Exception as e:
        return jsonify({
            'valid': False,
            'errors': [str(e)]
        })


@play_bp.route("/play/<story_name>")
def serve_compiled_story(story_name: str):
    """Serve a compiled HTML story."""
    # Basic sanitization - remove path traversal and dangerous chars
    # but keep the story name intact for file lookup
    safe_name = story_name.replace('../', '').replace('..\\', '').replace('/', '').replace('\\', '')
    safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '', safe_name)
    
    # Try to find the HTML file with various name formats
    html_path = OUTPUT_DIR / f"{safe_name}.html"
    
    if not html_path.exists():
        # Try replacing hyphens with underscores
        alt_name = safe_name.replace('-', '_')
        alt_html_path = OUTPUT_DIR / f"{alt_name}.html"
        if alt_html_path.exists():
            return send_file(alt_html_path, mimetype="text/html")
        
        # Try replacing underscores with hyphens
        alt_name2 = safe_name.replace('_', '-')
        alt_html_path2 = OUTPUT_DIR / f"{alt_name2}.html"
        if alt_html_path2.exists():
            return send_file(alt_html_path2, mimetype="text/html")
        
        abort(404, description=f"Compiled story not found: {safe_name}")
    
    return send_file(html_path, mimetype="text/html")
