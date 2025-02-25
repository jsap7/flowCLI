from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any
import subprocess
import shutil
import signal
import sys

class BaseTemplate(ABC):
    def __init__(self, project_name: str, features: List[str], target_dir: Path):
        self.project_name = project_name
        self.features = features
        self.target_dir = target_dir
        self._setup_interrupt_handler()
        
    def _setup_interrupt_handler(self):
        """Set up handler for SIGINT (Ctrl+C)."""
        def signal_handler(sig, frame):
            print("\n\nInterrupt received, cleaning up...")
            self._cleanup()
            sys.exit(1)
        
        signal.signal(signal.SIGINT, signal_handler)
    
    def _cleanup(self):
        """Clean up any created directories or files."""
        try:
            if self.target_dir.exists():
                shutil.rmtree(self.target_dir)
                print(f"\nCleaned up directory: {self.target_dir}")
        except Exception as e:
            print(f"\nError during cleanup: {e}")
    
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
            result = subprocess.run(cmd, check=True, cwd=cwd or self.target_dir)
            if result.returncode != 0:
                self._cleanup()
                return False
            return True
        except subprocess.CalledProcessError:
            self._cleanup()  # Clean up on command failure
            return False
        except KeyboardInterrupt:
            print("\n\nInterrupt received during command execution, cleaning up...")
            self._cleanup()
            sys.exit(1)
    
    def _copy_template(self, src: Path, dest: Path):
        """Copy template files."""
        if src.is_file():
            shutil.copy2(src, dest)
        else:
            shutil.copytree(src, dest, dirs_exist_ok=True)
    
    def open_in_cursor(self):
        """Open the project in Cursor."""
        try:
            self._run_command(["cursor", str(self.target_dir)])
        except Exception:
            # Don't clean up if Cursor fails to open - project was already created
            pass 