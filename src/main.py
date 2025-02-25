import typer
from rich.console import Console
from rich.panel import Panel
import questionary
import os
from pathlib import Path
import signal
import sys

from .config import ConfigManager
from .ui import UI
from .templates import (
    ReactTemplate,
    ReactSupabaseTemplate,
    PythonTemplate,
    NextjsTemplate,
    T3Template,
    FastAPITemplate,
    VueTemplate,
    DjangoTemplate
)

app = typer.Typer(
    name="flow",
    help="A CLI tool for smooth development workflows",
    add_completion=False,
)

new_app = typer.Typer(help="Create new projects")
app.add_typer(new_app, name="new")

console = Console()
config = ConfigManager()
ui = UI()

def setup_interrupt_handler():
    """Set up handler for SIGINT (Ctrl+C)."""
    def signal_handler(sig, frame):
        print("\n\nInterrupt received, exiting...")
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)

def get_template_class(project_type: str, framework: str = None):
    """Get the appropriate template class based on project type and framework."""
    if project_type == "React Frontend":
        return NextjsTemplate if framework == "next" else ReactTemplate
    elif project_type == "React + Supabase":
        return ReactSupabaseTemplate
    elif project_type == "T3 Stack":
        return T3Template
    elif project_type == "FastAPI Backend":
        return FastAPITemplate
    elif project_type == "Python Project":
        return PythonTemplate
    elif project_type == "Vue Frontend":
        return VueTemplate
    elif project_type == "Django Full-stack":
        return DjangoTemplate
    return None

@new_app.command("project")
def new_project():
    """Create a new project interactively."""
    try:
        setup_interrupt_handler()
        
        ui.print_header("🌊 Flow - New Project")
        
        # Get project name
        name = ui.get_project_name()
        if not name:
            ui.print_error("Project name is required")
            raise typer.Exit(1)
        
        # Get project category
        category = ui.select_category()
        if not category:
            ui.print_error("Project category is required")
            raise typer.Exit(1)
        
        # Get project type within category
        project_type = ui.select_project_type(category)
        if not project_type:
            ui.print_error("Project type is required")
            raise typer.Exit(1)
        
        # Get framework for React projects
        framework = None
        if project_type == "React Frontend":
            framework = ui.select_react_framework()
        
        # Get project features
        features = ui.select_features(project_type, framework)
        
        # Get template class
        template_class = get_template_class(project_type, framework)
        if not template_class:
            ui.print_error(f"Unknown project type: {project_type}")
            raise typer.Exit(1)
        
        # Create project
        config_data = config.load_config()
        target_dir = Path(os.path.expanduser(config_data.dev_folder)) / name
        
        if target_dir.exists():
            if not ui.confirm(f"Directory {target_dir} already exists. Overwrite?"):
                ui.print_error("Project creation cancelled.")
                raise typer.Exit(1)
            
            # Clean up existing directory
            import shutil
            shutil.rmtree(target_dir)
        
        # Initialize and generate project
        template = template_class(name, features, target_dir)
        if template.generate():
            ui.print_success(f"Project created successfully in {target_dir}")
            if config_data.ide == "cursor":
                template.open_in_cursor()
        else:
            ui.print_error("Failed to create project")
            raise typer.Exit(1)
            
    except KeyboardInterrupt:
        print("\n\nInterrupt received, exiting...")
        sys.exit(1)
    except Exception as e:
        ui.print_error(f"An error occurred: {str(e)}")
        raise typer.Exit(1)

@app.callback()
def callback():
    """Flow CLI - Smooth development workflows"""
    pass

def main():
    app()

if __name__ == "__main__":
    main()
