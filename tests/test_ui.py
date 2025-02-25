"""Tests for UI class."""
import pytest
from unittest.mock import patch, MagicMock
from src.ui import UI

@pytest.fixture
def ui():
    """Create a UI instance for testing."""
    return UI()

def test_project_categories(ui):
    """Test that project categories are properly defined."""
    assert len(ui.PROJECT_CATEGORIES) > 0
    for category in ui.PROJECT_CATEGORIES:
        assert "name" in category
        assert "display" in category
        assert "description" in category
        assert "value" in category

def test_project_templates(ui):
    """Test that project templates are properly defined."""
    assert len(ui.PROJECT_TEMPLATES) > 0
    for category, templates in ui.PROJECT_TEMPLATES.items():
        assert len(templates) > 0
        for template in templates:
            assert "name" in template
            assert "display" in template
            assert "description" in template
            assert "value" in template

def test_react_frameworks(ui):
    """Test that React frameworks are properly defined."""
    assert len(ui.REACT_FRAMEWORKS) > 0
    for framework in ui.REACT_FRAMEWORKS:
        assert "name" in framework
        assert "value" in framework

@patch('questionary.text')
def test_get_project_name(mock_text, ui):
    """Test project name input."""
    # Test valid name
    mock_text.return_value.ask.return_value = "test_project"
    assert ui.get_project_name() == "test_project"
    
    # Test empty name
    mock_text.return_value.ask.return_value = ""
    assert ui.get_project_name() == ""  # UI returns empty string for empty input
    
    # Test None
    mock_text.return_value.ask.return_value = None
    assert ui.get_project_name() is None  # UI returns None for None input

@patch('questionary.select')
def test_select_category(mock_select, ui):
    """Test category selection."""
    # Test valid selection
    mock_select.return_value.ask.return_value = "web"
    assert ui.select_category() == "web"
    
    # Test no selection
    mock_select.return_value.ask.return_value = None
    assert ui.select_category() is None

@patch('questionary.select')
def test_select_project_type(mock_select, ui):
    """Test project type selection."""
    # Test valid selection for web category
    mock_select.return_value.ask.return_value = "React Frontend"
    assert ui.select_project_type("web") == "React Frontend"
    
    # Test no selection
    mock_select.return_value.ask.return_value = None
    assert ui.select_project_type("web") is None
    
    # Test invalid category
    assert ui.select_project_type("invalid") is None

@patch('questionary.select')
def test_select_react_framework(mock_select, ui):
    """Test React framework selection."""
    # Test Next.js selection
    mock_select.return_value.ask.return_value = "next"
    assert ui.select_react_framework() == "next"
    
    # Test Vite selection
    mock_select.return_value.ask.return_value = "vite"
    assert ui.select_react_framework() == "vite"
    
    # Test no selection
    mock_select.return_value.ask.return_value = None
    assert ui.select_react_framework() is None

@patch('questionary.checkbox')
def test_select_features(mock_checkbox, ui):
    """Test feature selection."""
    features = ["TypeScript", "Tailwind CSS", "ESLint"]
    
    # Test selecting multiple features
    mock_checkbox.return_value.ask.return_value = features
    assert ui.select_features("React Frontend") == features
    
    # Test no features selected
    mock_checkbox.return_value.ask.return_value = []
    assert ui.select_features("React Frontend") == []
    
    # Test None returned
    mock_checkbox.return_value.ask.return_value = None
    assert ui.select_features("React Frontend") == []

@patch('questionary.confirm')
def test_confirm(mock_confirm, ui):
    """Test confirmation dialog."""
    # Test confirmation
    mock_confirm.return_value.ask.return_value = True
    assert ui.confirm("Are you sure?") is True
    
    # Test rejection
    mock_confirm.return_value.ask.return_value = False
    assert ui.confirm("Are you sure?") is False
    
    # Test no response
    mock_confirm.return_value.ask.return_value = None
    assert ui.confirm("Are you sure?") is None  # UI returns None for no response

@patch('rich.console.Console.print')
def test_print_methods(mock_print, ui):
    """Test print methods."""
    # Test print_header
    ui.print_header("Test Header")
    mock_print.assert_called()
    
    # Test print_success
    ui.print_success("Test Success")
    mock_print.assert_called()
    
    # Test print_error
    ui.print_error("Test Error")
    mock_print.assert_called()
    
    # Test print_info
    ui.print_info("Test Info")
    mock_print.assert_called()

@patch('questionary.checkbox')
def test_available_features(mock_checkbox, ui):
    """Test getting available features for different project types."""
    # Mock checkbox to return empty list to avoid interactive prompt
    mock_checkbox.return_value.ask.return_value = []
    
    # Test React Frontend features
    react_features = ui.select_features("React Frontend")
    assert isinstance(react_features, list)
    
    # Test Python Project features
    python_features = ui.select_features("Python Project")
    assert isinstance(python_features, list)
    
    # Test unknown project type
    unknown_features = ui.select_features("Unknown")
    assert isinstance(unknown_features, list)
    assert len(unknown_features) == 0 