"""Story CRUD operations router.
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import re

from backend.core.compiler import StoryCompiler
from backend.utils import is_safe_path, sanitize_filename

router = APIRouter()

# Get stories directory from project root
STORIES_DIR = Path(__file__).parent.parent.parent.parent / "stories"
OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "output"

class StorySaveRequest(BaseModel):
    content: str
    filename: str

class StoryDeleteRequest(BaseModel):
    filename: str

@router.get("/stories")
async def list_stories():
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
    
    return stories

@router.get("/story/{filename}")
async def get_story_content(filename: str):
    """Get raw content of a story file."""
    is_safe, story_path = is_safe_path(STORIES_DIR, filename)
    if not is_safe:
        raise HTTPException(status_code=403, detail="Invalid file path")
    
    if not story_path.exists() or not story_path.is_file():
        raise HTTPException(status_code=404, detail=f"Story not found: {filename}")
    
    try:
        with open(story_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {'content': content, 'filename': filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading story: {str(e)}")

@router.post("/save")
async def save_story(request: StorySaveRequest):
    """Save story to file."""
    filename = sanitize_filename(request.filename)
    
    is_safe, story_path = is_safe_path(STORIES_DIR, filename)
    if not is_safe:
        raise HTTPException(status_code=403, detail="Invalid filename")
    
    try:
        STORIES_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(story_path, 'w', encoding='utf-8') as f:
            f.write(request.content)
        
        return {
            'success': True,
            'message': f'Story saved as {filename}',
            'filename': filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete")
async def delete_story(request: StoryDeleteRequest):
    """Delete a story file."""
    if not request.filename:
        raise HTTPException(status_code=400, detail='No filename provided')
    
    is_safe, story_path = is_safe_path(STORIES_DIR, request.filename)
    if not is_safe:
        raise HTTPException(status_code=403, detail="Invalid filename")
    
    if not story_path.exists():
        raise HTTPException(status_code=404, detail='Story not found')
    
    try:
        story_path.unlink()
        return {
            'success': True,
            'message': f'Story {request.filename} deleted'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
