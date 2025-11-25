# GitHub Copilot Instructions for Pick-a-Page

> **Optimized for Claude Sonnet 4.5** | Last Updated: November 2025

## Project Overview

**Pick-a-Page** is an educational tool that helps children (ages 8+) create interactive "Choose Your Own Adventure" stories. The project transforms simple text files into beautiful, playable HTML stories with a modern scrolling narrative interface.

### Key Technologies

- **Backend**: Flask 2.3.0+ (Python 3.10+, WSGI)
- **Server**: Flask development server (use gunicorn for production)
- **Frontend**: Vanilla JavaScript (ES6+), CSS3 (mobile-first responsive)
- **Testing**: pytest 8.3.4+, pytest-cov (135 tests, 91% coverage)
- **Templating**: Jinja2 (server-side rendering)

## Architecture Principles

### 1. API-First Design

**All functionality must be exposed through REST API endpoints before adding UI.**

<principle>
API endpoints are the single source of truth. The web UI is a consumer of the API, not a replacement for it.
</principle>

#### Current API Structure

```
backend/
├── main.py                    # Flask app, middleware, health check
├── api/routers/              # REST API endpoints (Flask Blueprints)
│   ├── stories.py            # Story CRUD: GET, POST, PUT, DELETE
│   ├── compile_router.py     # Story compilation: text → HTML
│   ├── i18n.py              # Translation endpoints (15 languages)
│   ├── pages.py             # Frontend page serving
│   └── template.py          # Story initialization from templates
├── core/                     # Business logic (no HTTP concerns)
│   ├── compiler.py          # Parser, validator (130 lines)
│   ├── generator.py         # HTML/CSS/JS generator (72 lines)
│   ├── i18n.py             # 15-language translations (27 lines)
│   └── templates.py         # Story templates
└── utils/                    # Shared utilities
    └── file_utils.py        # Security: path validation, sanitization
```

#### API Design Requirements

When creating new endpoints:

1. **Clear HTTP verbs**: GET (read), POST (create), PUT (update), DELETE (remove)
2. **RESTful paths**: `/api/stories/{story_id}`, not `/api/getStory?id=123`
3. **Proper status codes**: 200 (success), 201 (created), 404 (not found), 400 (validation error), 500 (server error)
4. **Flask Blueprints**: Use Blueprint for modular route organization
5. **Error handling**: Return structured JSON errors with helpful messages

<example>
```python
from flask import Blueprint, jsonify, request, abort

bp = Blueprint('stories', __name__)

@bp.route("/stories", methods=["POST"])
def create_story():
    """Create a new story.
    
    Returns:
        dict: Created story with ID
        
    Raises:
        abort: If validation fails
    """
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")
    
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        abort(400, description="Title and content are required")
    
    try:
        # Business logic here
        return jsonify({"id": "story-123", "title": title}), 201
    except ValueError as e:
        abort(400, description=str(e))
```
</example>

### 2. Mobile-First Frontend

**All CSS and layouts must work on mobile devices (320px width) before desktop.**

<principle>
Design for the smallest screen first, then enhance for larger screens. Children often use tablets and phones.
</principle>

#### CSS Structure

```
backend/static/css/
├── layout.css        # Grid system, flexbox, mobile-first breakpoints
├── typography.css    # Font scales, line heights, responsive text
├── components.css    # Buttons, cards, forms (mobile optimized)
├── colors.css        # CSS variables for theming
├── mobile.css        # Mobile-specific overrides (<768px)
├── tablet.css        # Tablet layouts (768px-1024px)
├── desktop.css       # Desktop enhancements (>1024px)
└── story-player.css  # Story player (Squiffy-style scrolling)
```

#### Mobile-First CSS Pattern

```css
/* Base styles (mobile, 320px+) */
.story-card {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
    .story-card {
        width: 48%;
        padding: 1.5rem;
    }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .story-card {
        width: 32%;
        padding: 2rem;
        font-size: 1.125rem;
    }
}
```

#### Frontend Requirements

1. **Touch-friendly**: Buttons minimum 44×44px (iOS guideline)
2. **Readable**: Minimum 16px font size, 1.5 line height
3. **Fast**: Lazy load images, minimize reflows
4. **Accessible**: Semantic HTML, ARIA labels, keyboard navigation
5. **Progressive enhancement**: Works without JavaScript for core features

### 3. Test-Driven Development (TDD)

**Write tests BEFORE implementing features. Follow the RED → GREEN → REFACTOR cycle.**

<principle>
Tests are documentation. They explain what code should do and prevent regressions. Aim for 90%+ coverage.
</principle>

#### TDD Workflow

```
1. 🔴 RED: Write a failing test
2. 🟢 GREEN: Write minimal code to pass
3. 🔵 REFACTOR: Improve code quality
4. ♻️ REPEAT: Next test
```

#### Test Structure

```
tests/
├── core/                      # Core business logic tests
│   ├── test_compiler.py      # Parser, validator (42 tests)
│   ├── test_generator.py     # HTML generation (28 tests)
│   ├── test_i18n.py         # Translations (15 tests)
│   └── test_integration.py   # End-to-end (18 tests)
├── api/                       # API endpoint tests
│   ├── test_basic.py         # Health, pages, i18n (12 tests)
│   ├── test_stories.py       # Story CRUD (15 tests)
│   └── test_template.py      # Template init (5 tests)
└── fixtures/                  # Shared test data
    ├── valid_story.txt
    ├── broken_links.txt
    └── with_images.txt
```

#### Testing Requirements

<requirements>
1. **Test first**: Write tests before implementation
2. **One assertion per test**: Makes failures clear
3. **Descriptive names**: `test_compile_story_with_broken_links_raises_error()`
4. **Arrange-Act-Assert**: Clear test structure
5. **Use fixtures**: DRY principles apply to tests too
6. **Cleanup**: Use pytest fixtures to clean up test files
7. **Fast tests**: Parallelize when possible, mock I/O
8. **Coverage**: Maintain >85% (current: 91%)
</requirements>

<example>
```python
import pytest
from backend.core.compiler import compile_story

def test_compile_story_with_valid_content_succeeds():
    """Test that a valid story compiles without errors."""
    # ARRANGE
    content = """---
title: Test Story
author: Test Author
---

[[start]]
You begin your adventure.

[[Go forward]]

---

[[Go forward]]
You move forward.
"""
    
    # ACT
    result = compile_story(content)
    
    # ASSERT
    assert result.title == "Test Story"
    assert len(result.sections) == 2
    assert "start" in result.sections

def test_compile_story_with_broken_links_raises_error():
    """Test that broken links are detected during compilation."""
    # ARRANGE
    content = """---
title: Broken
---

[[start]]
Click [[nonexistent section]]
"""
    
    # ACT & ASSERT
    with pytest.raises(ValueError, match="Broken link"):
        compile_story(content)
```
</example>

#### Cleanup Fixtures

Always clean up test artifacts:

```python
import pytest
from pathlib import Path

@pytest.fixture
def cleanup_test_stories():
    """Clean up test stories after module completes."""
    yield
    
    # Cleanup runs after all tests in module
    stories_dir = Path("stories")
    test_files = [
        "test_story.txt",
        "test_compile.txt",
        "test_validation.txt"
    ]
    
    for filename in test_files:
        file_path = stories_dir / filename
        if file_path.exists():
            file_path.unlink()
    
    # Clean output directory
    output_dir = Path("output")
    if output_dir.exists():
        for html_file in output_dir.glob("test_*.html"):
            html_file.unlink()
```

### 4. SOLID Programming Principles

**Follow SOLID principles for maintainable, testable code.**

#### Single Responsibility Principle (SRP)

<principle>
Each module/class/function should do ONE thing well.
</principle>

<example>
```python
# ❌ BAD: Doing too much
def process_story(content):
    # Parsing
    sections = parse_sections(content)
    # Validation
    validate_links(sections)
    # Generation
    html = generate_html(sections)
    # File I/O
    write_file(html)
    return html

# ✅ GOOD: Separated concerns
def parse_story(content: str) -> Story:
    """Parse story content into data structure."""
    return Story(...)

def validate_story(story: Story) -> None:
    """Validate story structure and links."""
    check_broken_links(story)
    check_orphaned_sections(story)

def generate_html(story: Story) -> str:
    """Generate HTML from story data."""
    return render_template(story)
```
</example>

#### Open/Closed Principle (OCP)

<principle>
Open for extension, closed for modification. Use abstraction to add features.
</principle>

<example>
```python
# ✅ GOOD: Abstract base for validators
from abc import ABC, abstractmethod

class StoryValidator(ABC):
    @abstractmethod
    def validate(self, story: Story) -> list[str]:
        """Return list of validation errors."""
        pass

class BrokenLinkValidator(StoryValidator):
    def validate(self, story: Story) -> list[str]:
        errors = []
        for section in story.sections:
            for choice in section.choices:
                if choice.target not in story.sections:
                    errors.append(f"Broken link: {choice.target}")
        return errors

class OrphanedSectionValidator(StoryValidator):
    def validate(self, story: Story) -> list[str]:
        # Implementation
        pass

# Easy to add new validators without modifying existing code
def validate_story(story: Story, validators: list[StoryValidator]) -> list[str]:
    """Run all validators and collect errors."""
    errors = []
    for validator in validators:
        errors.extend(validator.validate(story))
    return errors
```
</example>

#### Liskov Substitution Principle (LSP)

<principle>
Subtypes must be substitutable for their base types without breaking functionality.
</principle>

#### Interface Segregation Principle (ISP)

<principle>
Don't force clients to depend on interfaces they don't use. Keep interfaces small and focused.
</principle>

#### Dependency Inversion Principle (DIP)

<principle>
Depend on abstractions (interfaces), not concrete implementations.
</principle>

<example>
```python
# ✅ GOOD: Depend on abstraction
from pathlib import Path
from typing import Protocol

class FileStorage(Protocol):
    """Abstract storage interface."""
    def save(self, filename: str, content: str) -> None: ...
    def load(self, filename: str) -> str: ...

class LocalFileStorage:
    """Concrete implementation for local filesystem."""
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
    
    def save(self, filename: str, content: str) -> None:
        (self.base_dir / filename).write_text(content)
    
    def load(self, filename: str) -> str:
        return (self.base_dir / filename).read_text()

# Easy to swap implementations (S3, database, etc.)
def save_story(story: Story, storage: FileStorage) -> None:
    """Save story using any storage implementation."""
    html = generate_html(story)
    storage.save(f"{story.title}.html", html)
```
</example>

### 5. Clean Code Practices

**Code should be readable, self-documenting, and maintainable.**

#### Naming Conventions

<rules>
- **Functions/methods**: Verb phrases (`compile_story`, `validate_links`, `generate_html`)
- **Classes**: Noun phrases (`Story`, `Section`, `StoryValidator`)
- **Variables**: Descriptive nouns (`story_content`, `section_name`, `choice_target`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_SECTION_LENGTH`, `DEFAULT_LANGUAGE`)
- **Private**: Leading underscore (`_internal_helper`)
- **Boolean variables**: Start with `is_`, `has_`, `should_` (`is_valid`, `has_images`)
</rules>

#### Function Length

<guideline>
Keep functions under 20 lines. If longer, extract helper functions.
</guideline>

<example>
```python
# ❌ BAD: Too long
def compile_story(content: str) -> Story:
    lines = content.split('\n')
    metadata = {}
    in_metadata = False
    for line in lines:
        if line.strip() == '---':
            in_metadata = not in_metadata
        elif in_metadata:
            key, value = line.split(':')
            metadata[key.strip()] = value.strip()
    # ... 50 more lines ...

# ✅ GOOD: Extracted helpers
def compile_story(content: str) -> Story:
    """Compile story text into Story object."""
    metadata = extract_metadata(content)
    sections = parse_sections(content)
    validate_story_structure(sections)
    return Story(metadata=metadata, sections=sections)

def extract_metadata(content: str) -> dict[str, str]:
    """Extract YAML metadata from story content."""
    # Implementation (< 20 lines)

def parse_sections(content: str) -> dict[str, Section]:
    """Parse story sections from content."""
    # Implementation (< 20 lines)
```
</example>

#### Comments and Docstrings

<guideline>
Code should be self-explanatory. Comments explain WHY, not WHAT.
</guideline>

<example>
```python
# ❌ BAD: Obvious comment
# Increment counter by 1
counter += 1

# ✅ GOOD: Explains WHY
# Skip first section (it's always 'start')
sections = sections[1:]

# ✅ EXCELLENT: Docstring with type hints
def sanitize_filename(
    filename: str,
    extension: str = ".txt",
    default: str = "story"
) -> str:
    """Sanitize filename for safe filesystem operations.
    
    Removes directory traversal attempts (../, /), dangerous characters,
    and ensures valid filename with proper extension.
    
    Args:
        filename: User-provided filename to sanitize
        extension: File extension to enforce (includes dot)
        default: Default name if filename is empty/invalid
        
    Returns:
        str: Safe filename suitable for filesystem operations
        
    Examples:
        >>> sanitize_filename("../../../etc/passwd")
        'story.txt'
        >>> sanitize_filename("my story!", ".html")
        'my_story.html'
    """
    # Implementation
```
</example>

#### DRY (Don't Repeat Yourself)

<principle>
Extract repeated code into functions. Current example: `backend/utils/file_utils.py`
</principle>

<example>
```python
# ❌ BAD: Repeated validation
def create_story(name: str):
    safe_name = name.replace("..", "").replace("/", "")
    # Use safe_name

def update_story(name: str):
    safe_name = name.replace("..", "").replace("/", "")
    # Use safe_name

# ✅ GOOD: Shared utility
from backend.utils.file_utils import sanitize_filename

def create_story(name: str):
    safe_name = sanitize_filename(name)
    # Use safe_name

def update_story(name: str):
    safe_name = sanitize_filename(name)
    # Use safe_name
```
</example>

## Security Requirements

<critical>
This is an educational tool for children. Security is paramount.
</critical>

### Path Traversal Prevention

**ALWAYS validate file paths to prevent directory traversal attacks.**

<example>
```python
from backend.utils.file_utils import is_safe_path

def get_story(story_name: str):
    """Get story content safely."""
    base_dir = Path("stories")
    requested_path = base_dir / story_name
    
    # REQUIRED: Check path safety
    if not is_safe_path(base_dir, requested_path):
        abort(400, description="Invalid story path")
    
    return requested_path.read_text()
```
</example>

### Filename Sanitization

**ALWAYS sanitize user-provided filenames.**

<example>
```python
from backend.utils.file_utils import sanitize_filename

@bp.route("/stories/init", methods=["POST"])
def initialize_story():
    """Initialize new story with template."""
    data = request.get_json()
    name = data.get('name', '')
    
    # REQUIRED: Sanitize user input
    safe_name = sanitize_filename(name, extension=".txt")
    
    story_path = Path("stories") / safe_name
    story_path.write_text(get_template())
    
    return jsonify({"filename": safe_name})
```
</example>

### Input Validation

**Validate input data in route handlers.**

<example>
```python
from flask import Blueprint, request, jsonify, abort

bp = Blueprint('stories', __name__)

@bp.route("/stories", methods=["POST"])
def create_story():
    """Create story with validated data."""
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")
    
    title = data.get('title', '').strip()
    author = data.get('author', '').strip()
    content = data.get('content', '').strip()
    
    # Validate required fields
    if not title or len(title) > 100:
        abort(400, description="Title is required (1-100 characters)")
    if not author or len(author) > 50:
        abort(400, description="Author is required (1-50 characters)")
    if not content or len(content) < 10:
        abort(400, description="Content must be at least 10 characters")
    
    # Prevent code injection in metadata
    for field in [title, author]:
        if any(char in field for char in ['<', '>', '&', '"', "'"]):
            abort(400, description="Special characters not allowed")
    
    # Create story...
    return jsonify({"title": title, "author": author})
```
</example>

## Internationalization (i18n)

**Support 15 languages with consistent translation keys.**

### Supported Languages

<languages>
English (en), Dutch (nl), Italian (it), Spanish (es), French (fr), Portuguese (pt), 
German (de), Russian (ru), Chinese (zh), Hindi (hi), Arabic (ar), Bengali (bn), 
Urdu (ur), Indonesian (id), Bulgarian (bg)
</languages>

### Translation Structure

```python
# backend/core/i18n.py
TRANSLATIONS = {
    "en": {
        "story_created": "Story created successfully",
        "invalid_format": "Invalid story format",
        "broken_links": "Story contains broken links"
    },
    "it": {
        "story_created": "Storia creata con successo",
        "invalid_format": "Formato storia non valido",
        "broken_links": "La storia contiene collegamenti interrotti"
    },
    # ... 13 more languages
}
```

### Translation Requirements

<requirements>
1. **Complete coverage**: All UI strings must have translations
2. **Consistent keys**: Use same key across all languages
3. **Fallback**: Default to English if translation missing
4. **Context**: Include context comments for translators
5. **Pluralization**: Handle singular/plural forms correctly
</requirements>

## File Organization

### Module Structure

```
backend/
├── main.py                    # Flask app entry point (50 lines)
├── core/                      # Business logic (no Flask/HTTP)
│   ├── __init__.py
│   ├── compiler.py           # Story parser + validator (130 lines)
│   ├── generator.py          # HTML generator (72 lines)
│   ├── i18n.py              # Translations (27 lines)
│   └── templates.py          # Story templates (3 lines)
├── api/routers/              # Flask Blueprints (HTTP layer only)
│   ├── __init__.py
│   ├── stories.py           # Story CRUD endpoints
│   ├── compile_router.py    # Compilation endpoints
│   ├── i18n.py             # Translation endpoints
│   ├── pages.py            # Frontend page serving
│   └── template.py         # Story initialization endpoints
├── utils/                    # Shared utilities
│   ├── __init__.py
│   └── file_utils.py        # Security utilities (107 lines)
├── static/                   # Frontend assets
│   ├── css/                 # 8 CSS files (841 lines total)
│   └── js/                  # 5 JS modules (888 lines total)
└── templates/               # Jinja2 templates
    └── index.html          # Main app interface
```

### Import Order (PEP 8)

```python
# 1. Standard library
from pathlib import Path
from typing import Optional
import json

# 2. Third-party packages
from flask import Blueprint, jsonify, request, abort
import pytest

# 3. Local application
from backend.core.compiler import compile_story
from backend.core.generator import generate_html
from backend.utils.file_utils import is_safe_path
```

## Common Patterns

### Error Handling in API Routes

<pattern>
```python
from flask import Blueprint, jsonify, abort
from pathlib import Path

bp = Blueprint('stories', __name__)

@bp.route("/stories/<story_id>")
def get_story(story_id: str):
    """Get story by ID with proper error handling."""
    try:
        # Validate input
        safe_id = sanitize_filename(story_id)
        story_path = Path("stories") / safe_id
        
        # Check existence
        if not story_path.exists():
            abort(404, description=f"Story '{story_id}' not found")
        
        # Check security
        if not is_safe_path(Path("stories"), story_path):
            abort(400, description="Invalid story path")
        
        # Business logic
        content = story_path.read_text()
        return jsonify({"id": safe_id, "content": content})
        
    except Exception as e:
        # Log unexpected errors
        print(f"Unexpected error in get_story: {e}")
        abort(500, description="Internal server error")
```
</pattern>

### File Operations

<pattern>
```python
from pathlib import Path

def read_story(story_path: Path) -> str:
    """Read story file."""
    with open(story_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_story(story_path: Path, content: str) -> None:
    """Write story file."""
    with open(story_path, 'w', encoding='utf-8') as f:
        f.write(content)
```
</pattern>

### Testing API Endpoints

<pattern>
```python
import pytest
from backend.main import app

@pytest.fixture
def client():
    """Create Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_story_returns_200(client):
    """Test story creation returns 200 OK."""
    # ARRANGE
    story_data = {
        "title": "Test Story",
        "author": "Test Author",
        "content": "Story content"
    }
    
    # ACT
    response = client.post("/api/stories", json=story_data)
    
    # ASSERT
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Test Story"

def test_get_nonexistent_story_returns_404(client):
    """Test getting non-existent story returns 404."""
    response = client.get("/api/stories/nonexistent")
    assert response.status_code == 404
```
</pattern>

## Code Review Checklist

Before submitting code, verify:

<checklist>
- [ ] **Tests written first** (TDD: RED → GREEN → REFACTOR)
- [ ] **All tests pass** (`make test` - 135+ tests)
- [ ] **Coverage >85%** (`make coverage` - currently 91%)
- [ ] **Type hints** on all function signatures
- [ ] **Docstrings** on public functions (Google style)
- [ ] **PEP 8 compliant** (`make lint`)
- [ ] **Security checks**: Path validation, filename sanitization
- [ ] **Error handling**: Proper HTTP status codes, helpful messages
- [ ] **Mobile-first**: CSS works at 320px width
- [ ] **API-first**: Business logic in `core/`, HTTP in `api/routers/`
- [ ] **SOLID principles**: Single responsibility, DRY
- [ ] **Cleanup fixtures**: Tests clean up after themselves
- [ ] **No console.log/print**: Use proper logging
- [ ] **Comments explain WHY**, not WHAT
- [ ] **Functions <20 lines**: Extract helpers if longer
</checklist>

## Development Workflow

### Starting Development

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start server
make serve
# Or: python -c "from backend.main import app; app.run(host='127.0.0.1', port=8001, debug=True)"

# 4. Run tests in watch mode (separate terminal)
make test-watch
# Or: ptw -- -v --cov=backend
```

### Adding a New Feature

<workflow>
1. **Write failing test** (RED)
   ```bash
   # Create test_new_feature.py
   pytest tests/api/test_new_feature.py -v
   # Test should FAIL
   ```

2. **Implement minimal code** (GREEN)
   ```bash
   # Write code in backend/api/routers/ or backend/core/
   pytest tests/api/test_new_feature.py -v
   # Test should PASS
   ```

3. **Refactor for quality** (REFACTOR)
   ```bash
   # Improve code structure, extract functions, add docs
   make lint
   make test
   make coverage
   ```

4. **Verify coverage**
   ```bash
   pytest --cov=backend --cov-report=term-missing
   # Check that new code is >85% covered
   ```

5. **Commit with descriptive message**
   ```bash
   git add .
   git commit -m "feat: add story export to PDF endpoint
   
   - Add POST /api/stories/{id}/export endpoint
   - Add PDF generation in core/pdf_generator.py
   - Add 8 tests covering success/error cases
   - Coverage: 94% (+3%)
   "
   ```
</workflow>

### Git Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

<example>
```
feat(api): add story export to PDF endpoint

- Implement POST /api/stories/{id}/export
- Add PDF generation using ReportLab
- Add 8 tests for success/error cases
- Update API documentation

Closes #42
```
</example>

## Performance Guidelines

### Backend Performance

<guidelines>
1. **Use Flask efficiently**: Minimize unnecessary processing in routes
2. **Cache static content**: Use Flask's `send_from_directory` with caching
3. **Lazy load**: Don't load all stories into memory
4. **Database ready**: Structure code for easy SQLite/PostgreSQL addition
5. **Pagination**: Return max 50 items per page
6. **Compression**: Enable gzip middleware for API responses
</guidelines>

### Frontend Performance

<guidelines>
1. **Minimize HTTP requests**: Bundle CSS/JS where appropriate
2. **Lazy load images**: Use `loading="lazy"` attribute
3. **Debounce input**: Don't validate on every keystroke
4. **Local storage**: Cache translations, reduce API calls
5. **CSS animations**: Use `transform` and `opacity` (GPU accelerated)
6. **Avoid layout thrashing**: Batch DOM reads/writes
</guidelines>

## Debugging Tips

### Backend Debugging

```python
# Use logging, not print
import logging
logger = logging.getLogger(__name__)

@bp.route("/stories", methods=["POST"])
def create_story():
    data = request.get_json()
    logger.info(f"Creating story: {data.get('title')}")
    logger.debug(f"Story content length: {len(data.get('content', ''))}")
    
    try:
        result = compile_story(data.get('content'))
        logger.info(f"Story compiled successfully")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Story compilation failed: {e}", exc_info=True)
        abort(500, description="Compilation failed")
```

### Frontend Debugging

```javascript
// Use console methods appropriately
console.info('App initialized');
console.warn('Deprecated function called');
console.error('Story compilation failed:', error);

// Group related logs
console.group('Story Compilation');
console.log('Input:', storyText);
console.log('Sections:', sections.length);
console.log('Validation:', errors);
console.groupEnd();
```

### Common Issues

<troubleshooting>
1. **CORS errors**: Check CORS configuration in main.py
2. **404 on static files**: Verify static folder path
3. **Tests fail randomly**: Check for race conditions, use fixtures
4. **Import errors**: Ensure `__init__.py` exists in all packages
5. **Coverage drops**: Check for uncovered branches (if/else, try/except)
</troubleshooting>

## Resources

### Documentation

- [Flask Docs](https://flask.palletsprojects.com/) - API framework
- [pytest Docs](https://docs.pytest.org/) - Testing framework
- [Jinja2 Docs](https://jinja.palletsprojects.com/) - Templating
- [MDN Web Docs](https://developer.mozilla.org/) - Frontend reference
- [PEP 8](https://pep8.org/) - Python style guide

### Project Files

- `README.md` - User documentation, setup instructions
- `STORY_GUIDE.md` - Story writing guide (3 languages)
- `Makefile` - Development shortcuts
- `.github/copilot-instructions.md` - This file

### Internal Documentation

Read these files to understand the architecture:

```bash
# Core business logic
backend/core/compiler.py      # Story parsing and validation
backend/core/generator.py     # HTML generation algorithm
backend/core/i18n.py         # Translation system

# Security utilities
backend/utils/file_utils.py  # Path validation, sanitization

# API examples
backend/api/routers/stories.py  # CRUD operations
backend/api/routers/compile_router.py  # Compilation flow

# Test examples
tests/api/test_stories.py    # API testing patterns
tests/core/test_compiler.py  # Business logic testing
```

## Project Goals and Values

<values>
1. **Education First**: Tool should be simple enough for 8-year-olds
2. **Safety**: No security vulnerabilities, appropriate content filters
3. **Accessibility**: Works on all devices, screen readers, keyboards
4. **Quality**: High test coverage, clean code, comprehensive docs
5. **Performance**: Fast load times, smooth interactions
6. **Maintainability**: Easy for new developers to understand
7. **Internationalization**: Support for global audience (15+ languages)
</values>

## Questions?

When in doubt:

1. **Check existing code**: Look for similar patterns in the codebase
2. **Read tests**: Tests document expected behavior
3. **Follow SOLID**: Keep concerns separated, functions small
4. **Test first**: Write failing test, then implement
5. **Security first**: Validate all user input, sanitize all output
6. **Mobile first**: Start with 320px width, enhance for larger screens
7. **API first**: Expose functionality via REST before adding UI

---

**Remember**: This is a teaching tool for children. Keep it simple, safe, and fun! 🎉

*Last updated: November 2025 | Maintained by the Pick-a-Page team*
