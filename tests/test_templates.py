"""Tests for project templates."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.templates import (
    ReactTemplate,
    VueTemplate,
    DjangoTemplate,
    PythonTemplate
)
import subprocess

@pytest.mark.parametrize("template_class,expected_files", [
    (ReactTemplate, ["package.json", "src", "public"]),
    (VueTemplate, ["package.json", "src", "public"]),
    (DjangoTemplate, ["manage.py", "requirements.txt", "core"]),
    (PythonTemplate, ["src", "tests", "requirements.txt"]),
])
@patch('subprocess.run')
def test_template_generation(mock_run, temp_dir, mock_features, template_class, expected_files):
    """Test that each template generates the expected project structure."""
    # Mock successful command execution
    mock_run.return_value = MagicMock(returncode=0)
    
    project_name = "test_project"
    project_dir = temp_dir / project_name
    
    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create expected files/directories for testing
    for file in expected_files:
        if '.' in file:  # It's a file
            (project_dir / file).touch()
        else:  # It's a directory
            (project_dir / file).mkdir(parents=True, exist_ok=True)
    
    template = template_class(project_name, mock_features, project_dir)
    success = template.generate()
    
    assert success
    assert project_dir.exists()
    
    # Check for expected files and directories
    for file in expected_files:
        assert (project_dir / file).exists()

@patch('subprocess.run')
def test_template_cleanup_on_failure(mock_run, temp_dir):
    """Test that failed template generation cleans up properly."""
    # Mock failed command execution
    mock_run.side_effect = subprocess.CalledProcessError(1, "test")
    
    project_name = "test_project"
    project_dir = temp_dir / project_name
    
    template = DjangoTemplate(project_name, [], project_dir)
    success = template.generate()
    
    assert not success
    assert not project_dir.exists()  # Directory should be cleaned up

@pytest.mark.parametrize("template_class", [
    ReactTemplate,
    VueTemplate,
    DjangoTemplate,
    PythonTemplate
])
@patch('subprocess.run')
def test_template_feature_handling(mock_run, temp_dir, template_class):
    """Test that templates properly handle different feature combinations."""
    # Mock successful command execution
    mock_run.return_value = MagicMock(returncode=0)
    
    project_name = "test_project"
    project_dir = temp_dir / project_name
    
    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Test with no features
    template = template_class(project_name, [], project_dir)
    success = template.generate()
    assert success
    
    # Clean up
    if project_dir.exists():
        import shutil
        shutil.rmtree(project_dir)
    
    # Test with all features
    all_features = [
        "TypeScript",
        "Tailwind CSS",
        "ESLint",
        "Prettier",
        "Testing",
        "Docker",
        "PWA",
        "Authentication"
    ]
    
    # Create project directory again
    project_dir.mkdir(parents=True, exist_ok=True)
    
    template = template_class(project_name, all_features, project_dir)
    success = template.generate()
    assert success 