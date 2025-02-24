import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

class Config(BaseModel):
    dev_folder: str = "~/Development"
    ide: str = "cursor"

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".flow"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_exists()
        
    def _ensure_config_exists(self):
        """Ensure config directory and file exist."""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.save_config(Config())
    
    def load_config(self) -> Config:
        """Load configuration from file."""
        try:
            config_data = json.loads(self.config_file.read_text())
            return Config(**config_data)
        except Exception:
            return Config()
    
    def save_config(self, config: Config):
        """Save configuration to file."""
        self.config_file.write_text(config.model_dump_json(indent=2))
    
    def update_config(self, **kwargs):
        """Update configuration with new values."""
        config = self.load_config()
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        self.save_config(config)
