"""Pytest configuration and shared fixtures."""
import os
import shutil
import tempfile
from pathlib import Path
import pytest

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_config(temp_dir):
    """Create a mock configuration for testing."""
    return {
        "dev_folder": str(temp_dir),
        "ide": "cursor"
    }

@pytest.fixture
def mock_features():
    """Return a set of mock features for testing templates."""
    return [
        "TypeScript",
        "Tailwind CSS",
        "ESLint",
        "Prettier"
    ] 