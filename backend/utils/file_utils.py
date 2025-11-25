"""File utility functions for path validation and filename sanitization."""

import re
from pathlib import Path


def is_safe_path(base_dir: Path, requested_path: str) -> tuple[bool, Path]:
    """
    Validate that requested_path is safe and within base_dir.
    
    Prevents directory traversal attacks by ensuring the resolved path
    stays within the base directory.
    
    Args:
        base_dir: Base directory to constrain paths within
        requested_path: User-provided path to validate
        
    Returns:
        Tuple of (is_safe: bool, resolved_path: Path)
        If not safe, returns (False, Path())
        
    Examples:
        >>> is_safe_path(Path('/app/stories'), 'my_story.txt')
        (True, Path('/app/stories/my_story.txt'))
        >>> is_safe_path(Path('/app/stories'), '../etc/passwd')
        (False, Path())
    """
    try:
        # Check for obvious traversal attempts
        if '..' in requested_path or requested_path.startswith('/'):
            return False, Path()
        
        # Check for path separators with traversal
        if '/' in requested_path or '\\' in requested_path:
            parts = requested_path.split('/')
            if any('..' in part or part.startswith('.') for part in parts):
                return False, Path()
        
        # Resolve full path and verify it's within base_dir
        full_path = (base_dir / requested_path).resolve()
        
        if not str(full_path).startswith(str(base_dir.resolve())):
            return False, Path()
        
        return True, full_path
    except (ValueError, OSError):
        return False, Path()


def sanitize_filename(filename: str, extension: str = '.txt', default: str = 'new_story') -> str:
    """
    Sanitize filename to prevent security issues.
    
    Removes path traversal attempts, restricts to safe characters,
    and ensures proper file extension.
    
    Args:
        filename: Original filename
        extension: Required file extension (default: '.txt')
        default: Default filename if input is empty/invalid
        
    Returns:
        Sanitized filename with proper extension
        
    Examples:
        >>> sanitize_filename('my story')
        'my_story.txt'
        >>> sanitize_filename('../../../etc/passwd')
        'etc_passwd.txt'
        >>> sanitize_filename('test.html', extension='.html')
        'test.html'
    """
    # Remove path traversal attempts
    filename = filename.replace('../', '').replace('..\\', '')
    
    # Remove directory separators
    filename = filename.replace('/', '_').replace('\\', '_')
    
    # Allow only alphanumeric, dash, underscore, dot
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    
    # Remove leading/trailing dots and underscores
    filename = filename.strip('._')
    
    # Ensure proper extension
    if not filename.endswith(extension):
        # Remove any existing extension first
        if '.' in filename:
            filename = filename.rsplit('.', 1)[0]
        filename += extension
    
    # Default if empty
    if not filename or filename == extension:
        filename = f'{default}{extension}'
    
    return filename
