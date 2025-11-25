"""Story compilation and validation router.
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.compiler import StoryCompiler
from backend.core.generator import HTMLGenerator
from backend.utils import sanitize_filename

router = APIRouter()

# Get output directory from project root
OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "output"

class CompileRequest(BaseModel):
    content: str
    filename: str

class ValidateRequest(BaseModel):
    content: str

@router.post("/compile")
async def compile_story(request: CompileRequest):
    """Compile story to HTML."""
    try:
        # Sanitize filename and convert to HTML filename
        story_name = sanitize_filename(request.filename, extension='', default='story')
        story_name = story_name.replace('.txt', '')
        
        # Parse and validate
        compiler = StoryCompiler()
        story = compiler.parse(request.content)
        errors = compiler.validate(story)
        
        if errors:
            return {
                'success': False,
                'errors': errors
            }
        
        # Generate HTML (use stories/ as base path for image resolution)
        generator = HTMLGenerator()
        stories_dir = Path(__file__).parent.parent.parent.parent / "stories"
        html_content = generator.generate(story, base_path=stories_dir)
        
        # Save to output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        html_path = OUTPUT_DIR / f"{story_name}.html"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return {
            'success': True,
            'message': 'Story compiled successfully',
            'play_url': f'/play/{story_name}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@router.post("/validate")
async def validate_story(request: ValidateRequest):
    """Validate story structure."""
    try:
        compiler = StoryCompiler()
        story = compiler.parse(request.content)
        errors = compiler.validate(story)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'sections': len(story.sections),
            'title': story.metadata.title,
            'author': story.metadata.author
        }
    except Exception as e:
        return {
            'valid': False,
            'errors': [str(e)]
        }

@router.get("/play/{story_name}")
async def serve_compiled_story(story_name: str):
    """Serve a compiled HTML story."""
    from fastapi.responses import FileResponse
    
    # Sanitize story name
    story_name = sanitize_filename(story_name, extension='', default='story')
    html_path = OUTPUT_DIR / f"{story_name}.html"
    
    if not html_path.exists():
        raise HTTPException(status_code=404, detail=f"Compiled story not found: {story_name}")
    
    return FileResponse(html_path, media_type="text/html")
