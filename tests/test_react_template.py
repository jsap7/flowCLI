"""Tests for React template."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from src.templates import ReactTemplate

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path

def test_basic_generation(temp_dir):
    """Test basic project generation without additional features."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        template = ReactTemplate("test-project", [], temp_dir)
        success = template.generate()
        
        assert success
        assert mock_run.call_count > 0

def test_tailwind_setup(temp_dir):
    """Test project generation with Tailwind CSS."""
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value = MagicMock(returncode=0)
        template = ReactTemplate("test-project", ["Tailwind CSS"], temp_dir)
        
        # Create necessary directories
        (temp_dir / "src").mkdir(parents=True, exist_ok=True)
        
        success = template.generate()
        assert success
        
        # Verify files were written with correct content
        written_content = [args[0] for args, _ in mock_write.call_args_list]
        assert any('@tailwind base' in content for content in written_content)
        assert any('content: [' in content and './src/**/*.{js,ts,jsx,tsx}' in content for content in written_content)

def test_linting_setup(temp_dir):
    """Test project generation with ESLint and Prettier."""
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value = MagicMock(returncode=0)
        template = ReactTemplate("test-project", ["ESLint", "Prettier"], temp_dir)
        
        # Create necessary directories
        (temp_dir / "src").mkdir(parents=True, exist_ok=True)
        
        success = template.generate()
        assert success
        
        # Verify files were written with correct content
        written_content = [args[0] for args, _ in mock_write.call_args_list]
        assert any('plugin:react/recommended' in content for content in written_content)
        assert any('singleQuote' in content for content in written_content)

def test_npm_install_failure(temp_dir):
    """Test handling of npm install failure."""
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.write_text') as mock_write:
        
        def mock_run_side_effect(args, **kwargs):
            if 'install' in args and 'create' not in args:
                result = MagicMock()
                result.returncode = 1
                return result
            result = MagicMock()
            result.returncode = 0
            return result
            
        mock_run.side_effect = mock_run_side_effect
        mock_write.return_value = None
        
        template = ReactTemplate("test-project", ["Tailwind CSS"], temp_dir)
        
        # Create necessary directories
        (temp_dir / "src").mkdir(parents=True, exist_ok=True)
        
        success = template.generate()
        assert not success

def test_file_write_error(temp_dir):
    """Test handling of file write errors."""
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.side_effect = PermissionError()
        
        template = ReactTemplate("test-project", ["Tailwind CSS"], temp_dir)
        
        # Create necessary directories
        (temp_dir / "src").mkdir(parents=True, exist_ok=True)
        
        success = template.generate()
        assert not success 