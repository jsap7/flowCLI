"""Tests for main.py."""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import signal
from typer.testing import CliRunner
import questionary
import shutil
from unittest.mock import call

from src.main import (
    get_template_class,
    setup_interrupt_handler,
    app,
    ReactTemplate,
    NextjsTemplate,
    ReactSupabaseTemplate,
    T3Template,
    FastAPITemplate,
    PythonTemplate,
    VueTemplate,
    DjangoTemplate
)

runner = CliRunner()

def test_get_template_class():
    """Test template class selection."""
    # Test React templates
    assert get_template_class("React Frontend") == ReactTemplate
    assert get_template_class("React Frontend", "next") == NextjsTemplate
    
    # Test other templates
    assert get_template_class("React + Supabase") == ReactSupabaseTemplate
    assert get_template_class("T3 Stack") == T3Template
    assert get_template_class("FastAPI Backend") == FastAPITemplate
    assert get_template_class("Python Project") == PythonTemplate
    assert get_template_class("Vue Frontend") == VueTemplate
    assert get_template_class("Django Full-stack") == DjangoTemplate
    
    # Test unknown type
    assert get_template_class("Unknown") is None

def test_setup_interrupt_handler():
    """Test interrupt handler setup."""
    with patch('signal.signal') as mock_signal:
        setup_interrupt_handler()
        mock_signal.assert_called_once_with(signal.SIGINT, mock_signal.call_args[0][1])

@patch('src.main.ui')
@patch('src.main.config')
@patch('shutil.rmtree')
@patch('src.main.PythonTemplate')
def test_new_project_success(mock_template_class, mock_rmtree, mock_config, mock_ui):
    """Test successful project creation."""
    # Mock UI responses
    mock_ui.get_project_name.return_value = "test_project"
    mock_ui.select_category.return_value = "web"
    mock_ui.select_project_type.return_value = "Python Project"
    mock_ui.select_features.return_value = []
    mock_ui.confirm.return_value = True
    
    # Mock config
    mock_config.load_config.return_value = MagicMock(
        dev_folder="~/test",
        ide="cursor"
    )
    
    # Mock template
    mock_template_instance = MagicMock()
    mock_template_instance.generate.return_value = True
    mock_template_class.return_value = mock_template_instance
    
    # Mock Path.exists
    with patch('pathlib.Path.exists', return_value=False):
        result = runner.invoke(app, ["new", "project"])
        assert result.exit_code == 0
        
        # Verify template was created with correct parameters
        mock_template_class.assert_called_once()
        mock_template_instance.generate.assert_called_once()
        mock_ui.print_success.assert_called_once()

@patch('src.main.ui')
@patch('src.main.config')
@patch('shutil.rmtree')
@patch('src.main.PythonTemplate')
def test_new_project_failure(mock_template_class, mock_rmtree, mock_config, mock_ui):
    """Test project creation failure."""
    # Mock UI responses
    mock_ui.get_project_name.return_value = "test_project"
    mock_ui.select_category.return_value = "web"
    mock_ui.select_project_type.return_value = "Python Project"
    mock_ui.select_features.return_value = []
    mock_ui.confirm.return_value = True
    
    # Mock config
    mock_config.load_config.return_value = MagicMock(
        dev_folder="~/test",
        ide="cursor"
    )
    
    # Mock template
    mock_template_instance = MagicMock()
    mock_template_instance.generate.return_value = False
    mock_template_class.return_value = mock_template_instance
    
    # Mock Path.exists
    with patch('pathlib.Path.exists', return_value=False):
        result = runner.invoke(app, ["new", "project"])
        assert result.exit_code == 1
        
        # Verify template was created and generate was called
        mock_template_class.assert_called_once()
        mock_template_instance.generate.assert_called_once()
        assert mock_ui.print_error.call_count == 2
        mock_ui.print_error.assert_has_calls([
            call('Failed to create project'),
            call('An error occurred: 1')
        ])

@patch('src.main.ui')
def test_new_project_missing_name(mock_ui):
    """Test project creation with missing name."""
    # Mock UI responses
    mock_ui.get_project_name.return_value = None
    
    result = runner.invoke(app, ["new", "project"])
    assert result.exit_code == 1
    assert mock_ui.print_error.call_count == 2
    mock_ui.print_error.assert_has_calls([
        call('Project name is required'),
        call('An error occurred: 1')
    ])

@patch('src.main.ui')
def test_new_project_missing_category(mock_ui):
    """Test project creation with missing category."""
    # Mock UI responses
    mock_ui.get_project_name.return_value = "test_project"
    mock_ui.select_category.return_value = None
    
    result = runner.invoke(app, ["new", "project"])
    assert result.exit_code == 1
    assert mock_ui.print_error.call_count == 2
    mock_ui.print_error.assert_has_calls([
        call('Project category is required'),
        call('An error occurred: 1')
    ])

@patch('src.main.ui')
def test_new_project_missing_type(mock_ui):
    """Test project creation with missing project type."""
    # Mock UI responses
    mock_ui.get_project_name.return_value = "test_project"
    mock_ui.select_category.return_value = "web"
    mock_ui.select_project_type.return_value = None
    
    result = runner.invoke(app, ["new", "project"])
    assert result.exit_code == 1
    assert mock_ui.print_error.call_count == 2
    mock_ui.print_error.assert_has_calls([
        call('Project type is required'),
        call('An error occurred: 1')
    ])

@patch('src.main.ui')
@patch('src.main.config')
@patch('shutil.rmtree')
def test_new_project_existing_directory(mock_rmtree, mock_config, mock_ui):
    """Test project creation with existing directory."""
    # Mock UI responses
    mock_ui.get_project_name.return_value = "test_project"
    mock_ui.select_category.return_value = "web"
    mock_ui.select_project_type.return_value = "Python Project"
    mock_ui.select_features.return_value = []
    mock_ui.confirm.return_value = False
    
    # Mock config
    mock_config.load_config.return_value = MagicMock(
        dev_folder="~/test",
        ide="cursor"
    )
    
    # Mock Path.exists
    with patch('pathlib.Path.exists', return_value=True):
        result = runner.invoke(app, ["new", "project"])
        assert result.exit_code == 1
        assert mock_ui.print_error.call_count == 2
        mock_ui.print_error.assert_has_calls([
            call('Project creation cancelled.'),
            call('An error occurred: 1')
        ])

@patch('src.main.ui')
@patch('src.main.config')
@patch('shutil.rmtree')
@patch('src.main.NextjsTemplate')
def test_new_project_react_framework(mock_template_class, mock_rmtree, mock_config, mock_ui):
    """Test React project creation with framework selection."""
    # Mock UI responses
    mock_ui.get_project_name.return_value = "test_project"
    mock_ui.select_category.return_value = "web"
    mock_ui.select_project_type.return_value = "React Frontend"
    mock_ui.select_react_framework.return_value = "next"
    mock_ui.select_features.return_value = []
    mock_ui.confirm.return_value = True
    
    # Mock config
    mock_config.load_config.return_value = MagicMock(
        dev_folder="~/test",
        ide="cursor"
    )
    
    # Mock template
    mock_template_instance = MagicMock()
    mock_template_instance.generate.return_value = True
    mock_template_class.return_value = mock_template_instance
    
    # Mock Path.exists
    with patch('pathlib.Path.exists', return_value=False):
        result = runner.invoke(app, ["new", "project"])
        assert result.exit_code == 0
        
        # Verify NextjsTemplate was used
        mock_template_class.assert_called_once()
        mock_template_instance.generate.assert_called_once()
        mock_ui.print_success.assert_called_once() 