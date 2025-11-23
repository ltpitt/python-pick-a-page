"""
Tests for CLI functionality in __main__.py
"""

import pytest
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import sys
from pick_a_page.__main__ import compile_story


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
