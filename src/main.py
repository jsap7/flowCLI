import typer
from rich.console import Console
from rich.panel import Panel
import questionary
import os
from pathlib import Path

from .config import ConfigManager
from .ui import UI
from .templates import ReactTemplate, ReactSupabaseTemplate, PythonTemplate

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

def get_template_class(project_type: str):
    """Get the appropriate template class based on project type."""
    return {
        "React Frontend": ReactTemplate,
        "React + Supabase": ReactSupabaseTemplate,
        "Python Project": PythonTemplate
    }.get(project_type)

@new_app.command("project")
def new_project():
    """Create a new project interactively."""
    ui.print_header("🌊 Flow - New Project")
    
    # Get project name
    name = ui.get_project_name()
    if not name:
        ui.print_error("Project name is required")
        raise typer.Exit(1)
    
    # Get project type
    project_type = ui.select_project_type()
    
    # Get project features
    features = ui.select_features(project_type)
    
    # Get template class
    template_class = get_template_class(project_type)
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
    
    # Initialize and generate project
    template = template_class(name, features, target_dir)
    if template.generate():
        ui.print_success(f"Project created successfully in {target_dir}")
        if config_data.ide == "cursor":
            template.open_in_cursor()
    else:
        ui.print_error("Failed to create project")
        raise typer.Exit(1)

@app.callback()
def callback():
    """Flow CLI - Smooth development workflows"""
    pass

def main():
    app()

if __name__ == "__main__":
    main()
