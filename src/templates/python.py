from pathlib import Path
from typing import List
from .base import BaseTemplate

class PythonTemplate(BaseTemplate):
    def generate(self):
        """Generate a Python project structure."""
        # Create project structure
        src_dir = self.target_dir / "src"
        tests_dir = self.target_dir / "tests"
        
        self._create_directory(src_dir)
        self._create_directory(tests_dir)
        
        # Create main.py
        main_content = """class MyProject:
    def __init__(self):
        self.name = "MyProject"
    
    def hello(self):
        return f"Hello from {self.name}!"

def main():
    project = MyProject()
    print(project.hello())

if __name__ == "__main__":
    main()
"""
        self._write_file(src_dir / "main.py", main_content)
        
        # Create __init__.py files
        self._write_file(src_dir / "__init__.py", "")
        self._write_file(tests_dir / "__init__.py", "")
        
        # Create requirements.txt
        requirements = """pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
"""
        self._write_file(self.target_dir / "requirements.txt", requirements)
        
        # Create README.md
        readme = f"""# {self.project_name}

A Python project created with Flow CLI.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```bash
python src/main.py
```

## Testing

Run tests with pytest:
```bash
pytest tests/
```
"""
        self._write_file(self.target_dir / "README.md", readme)
        
        # Create test file
        test_content = """import pytest
from src.main import MyProject

def test_hello():
    project = MyProject()
    assert project.hello() == "Hello from MyProject!"
"""
        self._write_file(tests_dir / "test_main.py", test_content)
        
        return True
