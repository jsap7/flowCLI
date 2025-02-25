"""Tests for configuration management."""
import pytest
from pathlib import Path
from src.config import Config, ConfigManager

def test_config_default_values():
    """Test default configuration values."""
    config = Config()
    assert config.dev_folder == "~/Development"
    assert config.ide == "cursor"

def test_config_custom_values():
    """Test custom configuration values."""
    config = Config(dev_folder="/custom/path", ide="vscode")
    assert config.dev_folder == "/custom/path"
    assert config.ide == "vscode"

def test_config_manager_save_load(temp_dir, monkeypatch):
    """Test saving and loading configuration."""
    # Mock home directory
    monkeypatch.setattr(Path, "home", lambda: temp_dir)
    
    manager = ConfigManager()
    config = Config(dev_folder="/test/path", ide="vscode")
    
    # Test save
    manager.save_config(config)
    assert manager.config_file.exists()
    
    # Test load
    loaded_config = manager.load_config()
    assert loaded_config.dev_folder == "/test/path"
    assert loaded_config.ide == "vscode"

def test_config_manager_update(temp_dir, monkeypatch):
    """Test updating configuration values."""
    # Mock home directory
    monkeypatch.setattr(Path, "home", lambda: temp_dir)
    
    manager = ConfigManager()
    manager.update_config(dev_folder="/new/path")
    
    config = manager.load_config()
    assert config.dev_folder == "/new/path"
    assert config.ide == "cursor"  # Default value should remain 