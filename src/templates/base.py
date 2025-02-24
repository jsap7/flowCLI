from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any
import subprocess
import shutil

class BaseTemplate(ABC):
    def __init__(self, project_name: str, features: List[str], target_dir: Path):
        self.project_name = project_name
        self.features = features
        self.target_dir = target_dir
        
    @abstractmethod
    def generate(self):
        """Generate the project structure."""
        pass
    
    def _create_directory(self, path: Path):
        """Create a directory if it doesn't exist."""
        path.mkdir(parents=True, exist_ok=True)
    
    def _write_file(self, path: Path, content: str):
        """Write content to a file."""
        path.write_text(content)
    
    def _run_command(self, cmd: List[str], cwd: Path = None) -> bool:
        """Run a shell command."""
        try:
            subprocess.run(cmd, check=True, cwd=cwd or self.target_dir)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _copy_template(self, src: Path, dest: Path):
        """Copy template files."""
        if src.is_file():
            shutil.copy2(src, dest)
        else:
            shutil.copytree(src, dest, dirs_exist_ok=True)
    
    def open_in_cursor(self):
        """Open the project in Cursor."""
        self._run_command(["cursor", str(self.target_dir)]) 