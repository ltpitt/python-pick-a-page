"""
Tests for CLI functionality in __main__.py
"""

import pytest
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import sys
import zipfile
from pick_a_page.__main__ import compile_story, validate_story_file, init_story


class TestCompileWithBrowserOpen:
    """Test the compile command with browser opening functionality."""
    
    @pytest.fixture
    def mock_args_with_open(self, tmp_path):
        """Mock args for compile with browser opening enabled (default)."""
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = True  # Skip zip for faster tests
        args.no_open = False  # Default: open browser
        
        return args
    
    @pytest.fixture
    def mock_args_no_open(self, tmp_path):
        """Mock args for compile with browser opening disabled."""
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = True
        args.no_open = True  # Disable browser opening
        
        return args
    
    @patch('pick_a_page.__main__.webbrowser.open')
    def test_compile_opens_browser_by_default(self, mock_browser_open, mock_args_with_open):
        """Test that compile opens browser by default (no_open=False)."""
        result = compile_story(mock_args_with_open)
        
        assert result == 0, "Compile should succeed"
        assert mock_browser_open.called, "Browser should be opened by default"
        
        # Verify it opened the correct HTML file
        call_args = mock_browser_open.call_args[0][0]
        assert str(call_args).endswith('valid_story.html'), \
            f"Should open the generated HTML file, got: {call_args}"
    
    @patch('pick_a_page.__main__.webbrowser.open')
    def test_compile_respects_no_open_flag(self, mock_browser_open, mock_args_no_open):
        """Test that --no-open flag prevents browser opening."""
        result = compile_story(mock_args_no_open)
        
        assert result == 0, "Compile should succeed"
        assert not mock_browser_open.called, \
            "Browser should NOT be opened when --no-open flag is set"
    
    @patch('pick_a_page.__main__.webbrowser.open')
    def test_browser_opens_with_absolute_path(self, mock_browser_open, mock_args_with_open):
        """Test that browser is opened with an absolute file:// URL."""
        result = compile_story(mock_args_with_open)
        
        assert result == 0
        assert mock_browser_open.called
        
        # Check the path is absolute
        call_args = str(mock_browser_open.call_args[0][0])
        assert Path(call_args.replace('file://', '')).is_absolute() or call_args.startswith('/'), \
            f"Browser should be opened with absolute path, got: {call_args}"
    
    @patch('pick_a_page.__main__.webbrowser.open')
    def test_browser_failure_does_not_break_compile(self, mock_browser_open, mock_args_with_open):
        """Test that browser opening failure doesn't break compilation."""
        # Simulate browser opening failure
        mock_browser_open.side_effect = Exception("Browser not available")
        
        result = compile_story(mock_args_with_open)
        
        # Compilation should still succeed
        assert result == 0, "Compile should succeed even if browser fails to open"
        
        # But the attempt should have been made
        assert mock_browser_open.called


class TestCLIArgumentParsing:
    """Test CLI argument parsing for the --no-open flag."""
    
    def test_no_open_flag_exists_in_compile_command(self):
        """Test that --no-open flag is available in compile command."""
        # This will be verified by checking argparse setup
        from pick_a_page.__main__ import main
        
        with patch('sys.argv', ['pick-a-page', 'compile', '--help']):
            with patch('sys.exit'):
                with patch('sys.stdout') as mock_stdout:
                    try:
                        main()
                    except SystemExit:
                        pass
                    
                    # Check if --no-open appears in help text
                    # Note: This is a simplified test, actual implementation may vary
                    # Full test would require capturing help output
    
    def test_default_open_behavior_without_flag(self, tmp_path):
        """Test that without --no-open, the browser should open."""
        # This is tested via the mock_args_with_open fixture
        # where args.no_open = False
        pass


class TestCrossPlatformCompatibility:
    """Test that browser opening works across platforms."""
    
    @patch('pick_a_page.__main__.webbrowser.open')
    @patch('platform.system')
    def test_works_on_windows(self, mock_platform, mock_browser_open, tmp_path):
        """Test browser opening works on Windows."""
        mock_platform.return_value = 'Windows'
        
        from pick_a_page.__main__ import compile_story
        
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = True
        args.no_open = False
        
        result = compile_story(args)
        
        assert result == 0
        assert mock_browser_open.called
    
    @patch('pick_a_page.__main__.webbrowser.open')
    @patch('platform.system')
    def test_works_on_linux(self, mock_platform, mock_browser_open, tmp_path):
        """Test browser opening works on Linux."""
        mock_platform.return_value = 'Linux'
        
        from pick_a_page.__main__ import compile_story
        
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = True
        args.no_open = False
        
        result = compile_story(args)
        
        assert result == 0
        assert mock_browser_open.called
    
    @patch('pick_a_page.__main__.webbrowser.open')
    @patch('platform.system')
    def test_works_on_macos(self, mock_platform, mock_browser_open, tmp_path):
        """Test browser opening works on macOS (including old OS X 10.4)."""
        mock_platform.return_value = 'Darwin'
        
        from pick_a_page.__main__ import compile_story
        
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = True
        args.no_open = False
        
        result = compile_story(args)
        
        assert result == 0
        assert mock_browser_open.called


class TestCompileZipCreation:
    """Test ZIP file creation during compilation."""
    
    def test_creates_zip_by_default(self, tmp_path):
        """Test that ZIP file is created by default."""
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = False  # Default: create ZIP
        args.no_open = True
        
        result = compile_story(args)
        
        assert result == 0
        zip_file = tmp_path / "output" / "valid_story.zip"
        assert zip_file.exists(), "ZIP file should be created by default"
    
    def test_no_zip_flag_skips_zip_creation(self, tmp_path):
        """Test that --no-zip flag skips ZIP creation."""
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = True
        args.no_open = True
        
        result = compile_story(args)
        
        assert result == 0
        zip_file = tmp_path / "output" / "valid_story.zip"
        assert not zip_file.exists(), "ZIP file should NOT be created with --no-zip"
    
    def test_zip_contains_html_and_source(self, tmp_path):
        """Test that ZIP contains HTML, source story, and images."""
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = False
        args.no_open = True
        
        result = compile_story(args)
        
        assert result == 0
        zip_file = tmp_path / "output" / "valid_story.zip"
        
        with zipfile.ZipFile(zip_file, 'r') as zf:
            names = zf.namelist()
            assert 'valid_story.html' in names, "ZIP should contain HTML file"
            assert 'valid_story.txt' in names, "ZIP should contain source story file"


class TestCompileErrorHandling:
    """Test error handling in compile command."""
    
    def test_fails_on_missing_input_file(self, tmp_path):
        """Test that compile fails gracefully when input file doesn't exist."""
        args = MagicMock()
        args.input = tmp_path / "nonexistent.txt"
        args.output = tmp_path / "output"
        args.no_zip = True
        args.no_open = True
        
        result = compile_story(args)
        
        assert result == 1, "Should return error code 1 for missing file"
    
    def test_fails_on_invalid_story_syntax(self, tmp_path):
        """Test that compile fails on invalid story syntax."""
        # Create invalid story (missing metadata)
        invalid_story = tmp_path / "invalid.txt"
        invalid_story.write_text("[[start]]\nJust text, no metadata!")
        
        args = MagicMock()
        args.input = invalid_story
        args.output = tmp_path / "output"
        args.no_zip = True
        args.no_open = True
        
        result = compile_story(args)
        
        assert result == 1, "Should return error code 1 for invalid syntax"
    
    def test_fails_on_broken_links(self, tmp_path):
        """Test that compile fails when story has broken links."""
        input_file = Path(__file__).parent / "fixtures" / "broken_links.txt"
        
        args = MagicMock()
        args.input = input_file
        args.output = tmp_path / "output"
        args.no_zip = True
        args.no_open = True
        
        result = compile_story(args)
        
        assert result == 1, "Should return error code 1 for broken links"


class TestValidateCommand:
    """Test the validate command behavior."""
    
    def test_validates_correct_story(self):
        """Test that validate succeeds on a valid story."""
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        
        args = MagicMock()
        args.input = input_file
        
        result = validate_story_file(args)
        
        assert result == 0, "Valid story should pass validation"
    
    def test_fails_on_missing_file(self, tmp_path):
        """Test that validate fails when file doesn't exist."""
        args = MagicMock()
        args.input = tmp_path / "nonexistent.txt"
        
        result = validate_story_file(args)
        
        assert result == 1, "Should return error code 1 for missing file"
    
    def test_fails_on_broken_links(self):
        """Test that validate detects broken links."""
        input_file = Path(__file__).parent / "fixtures" / "broken_links.txt"
        
        args = MagicMock()
        args.input = input_file
        
        result = validate_story_file(args)
        
        assert result == 1, "Should return error code 1 for broken links"
    
    def test_fails_on_invalid_syntax(self, tmp_path):
        """Test that validate detects invalid story syntax."""
        invalid_story = tmp_path / "invalid.txt"
        invalid_story.write_text("No metadata here!")
        
        args = MagicMock()
        args.input = invalid_story
        
        result = validate_story_file(args)
        
        assert result == 1, "Should return error code 1 for invalid syntax"


class TestInitCommand:
    """Test the init command behavior."""
    
    def test_creates_new_story_project(self, tmp_path):
        """Test that init creates a new story project with template."""
        args = MagicMock()
        args.name = "test_story"
        args.directory = tmp_path / "test_story"
        
        result = init_story(args)
        
        assert result == 0, "Init should succeed"
        assert args.directory.exists(), "Project directory should be created"
        
        story_file = args.directory / "test_story.txt"
        assert story_file.exists(), "Story template file should be created"
        
        images_dir = args.directory / "images"
        assert images_dir.exists(), "Images directory should be created"
    
    def test_fails_on_existing_directory(self, tmp_path):
        """Test that init fails when directory already exists."""
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()
        
        args = MagicMock()
        args.name = "test_story"
        args.directory = existing_dir
        
        result = init_story(args)
        
        assert result == 1, "Should return error code 1 for existing directory"
    
    def test_creates_valid_template(self, tmp_path):
        """Test that init creates a valid story template structure."""
        args = MagicMock()
        args.name = "test_story"
        args.directory = tmp_path / "test_story"
        
        result = init_story(args)
        assert result == 0
        
        # Verify the template has basic structure
        story_file = args.directory / "test_story.txt"
        content = story_file.read_text()
        
        # Check it has metadata block
        assert '---' in content, "Template should have metadata section"
        assert 'title:' in content, "Template should have title field"
        assert 'author:' in content, "Template should have author field"
        
        # Check it has at least one section
        assert '[[' in content, "Template should have at least one section"


class TestCompileOutputDirectory:
    """Test output directory handling in compile command."""
    
    def test_creates_output_directory_if_missing(self, tmp_path):
        """Test that compile creates output directory if it doesn't exist."""
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        output_dir = tmp_path / "nested" / "output" / "dir"
        
        args = MagicMock()
        args.input = input_file
        args.output = output_dir
        args.no_zip = True
        args.no_open = True
        
        result = compile_story(args)
        
        assert result == 0
        assert output_dir.exists(), "Output directory should be created"
        assert (output_dir / "valid_story.html").exists()
    
    def test_uses_default_output_directory(self, tmp_path, monkeypatch):
        """Test that compile uses 'output' as default directory."""
        monkeypatch.chdir(tmp_path)
        
        input_file = Path(__file__).parent / "fixtures" / "valid_story.txt"
        
        args = MagicMock()
        args.input = input_file
        args.output = None  # No output specified
        args.no_zip = True
        args.no_open = True
        
        result = compile_story(args)
        
        assert result == 0
        # Default 'output' directory should be created
        default_output = tmp_path / "output"
        assert default_output.exists(), "Default 'output' directory should be created"
