"""Tests for base template class."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import subprocess
import signal
import sys
import shutil
from src.templates.base import BaseTemplate
from typing import List

# Mock implementation of BaseTemplate for testing
def create_mock_template(project_name: str, features: List[str], target_dir: Path) -> BaseTemplate:
    class MockTemplate(BaseTemplate):
        def generate(self):
            """Test implementation of generate method."""
            return True
    return MockTemplate(project_name, features, target_dir)

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path

@pytest.fixture
def template(temp_dir):
    """Create a test template instance."""
    return create_mock_template("test_project", [], temp_dir)

def test_init(template):
    """Test template initialization."""
    assert template.project_name == "test_project"
    assert template.features == []
    assert isinstance(template.target_dir, Path)

def test_cleanup(template, temp_dir):
    """Test cleanup functionality."""
    # Create a test file
    test_file = temp_dir / "test.txt"
    test_file.write_text("test")
    
    # Test cleanup
    template._cleanup()
    assert not temp_dir.exists()

def test_cleanup_error(template, temp_dir):
    """Test cleanup with error."""
    with patch('shutil.rmtree') as mock_rmtree:
        mock_rmtree.side_effect = PermissionError("Permission denied")
        
        # Should not raise an exception
        template._cleanup()

def test_create_directory(template, temp_dir):
    """Test directory creation."""
    test_dir = temp_dir / "test_dir"
    template._create_directory(test_dir)
    assert test_dir.exists()
    assert test_dir.is_dir()

def test_create_directory_error(template, temp_dir):
    """Test directory creation with error."""
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        mock_mkdir.side_effect = PermissionError("Permission denied")
        
        # Should raise an exception
        with pytest.raises(PermissionError):
            template._create_directory(temp_dir / "test_dir")

def test_write_file(template, temp_dir):
    """Test file writing."""
    test_file = temp_dir / "test.txt"
    content = "test content"
    template._write_file(test_file, content)
    
    assert test_file.exists()
    assert test_file.read_text() == content

def test_write_file_error(template, temp_dir):
    """Test file writing with error."""
    with patch('pathlib.Path.write_text') as mock_write:
        mock_write.side_effect = PermissionError("Permission denied")
        
        # Should raise an exception
        with pytest.raises(PermissionError):
            template._write_file(temp_dir / "test.txt", "test")

def test_run_command_success(template):
    """Test successful command execution."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template._run_command(["echo", "test"])
        assert success
        mock_run.assert_called_once()

def test_run_command_failure(template):
    """Test command execution failure."""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "test")
        
        success = template._run_command(["test"])
        assert not success

def test_run_command_keyboard_interrupt(template):
    """Test command execution with keyboard interrupt."""
    with patch('subprocess.run') as mock_run, \
         patch('sys.exit') as mock_exit:
        mock_run.side_effect = KeyboardInterrupt()
        
        template._run_command(["test"])
        mock_exit.assert_called_once_with(1)

def test_copy_template_file(template, temp_dir):
    """Test copying a single file."""
    src_file = temp_dir / "src.txt"
    src_file.write_text("test")
    
    dest_file = temp_dir / "dest.txt"
    
    template._copy_template(src_file, dest_file)
    assert dest_file.exists()
    assert dest_file.read_text() == "test"

def test_copy_template_directory(template, temp_dir):
    """Test copying a directory."""
    src_dir = temp_dir / "src"
    src_dir.mkdir()
    (src_dir / "test.txt").write_text("test")
    
    dest_dir = temp_dir / "dest"
    
    template._copy_template(src_dir, dest_dir)
    assert dest_dir.exists()
    assert (dest_dir / "test.txt").exists()
    assert (dest_dir / "test.txt").read_text() == "test"

def test_copy_template_error(template, temp_dir):
    """Test template copying with error."""
    # Create source file
    src_file = temp_dir / "src.txt"
    src_file.write_text("test")
    
    with patch('shutil.copy2') as mock_copy:
        mock_copy.side_effect = PermissionError("Permission denied")
        
        # Should raise an exception
        with pytest.raises(PermissionError):
            template._copy_template(src_file, temp_dir / "dest.txt")

def test_open_in_cursor(template):
    """Test opening project in Cursor."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        template.open_in_cursor()
        mock_run.assert_called_once()

def test_open_in_cursor_error(template):
    """Test opening project in Cursor with error."""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = Exception("Failed to open")
        
        # Should not raise an exception
        template.open_in_cursor()

def test_interrupt_handler(template):
    """Test interrupt handler setup."""
    with patch('signal.signal') as mock_signal:
        template._setup_interrupt_handler()
        mock_signal.assert_called_once_with(signal.SIGINT, mock_signal.call_args[0][1])

def test_interrupt_handler_cleanup(template, temp_dir):
    """Test interrupt handler cleanup."""
    with patch('sys.exit') as mock_exit:
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test")
        
        # Get the handler
        handler = signal.getsignal(signal.SIGINT)
        
        # Call the handler
        handler(signal.SIGINT, None)
        
        # Check cleanup and exit
        assert not temp_dir.exists()
        mock_exit.assert_called_once_with(1) 