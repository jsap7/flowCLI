from typing import List, Dict, Any
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich import box
from rich.text import Text

console = Console()

class UI:
    # Styles
    HEADER_STYLE = Style(color="blue", bold=True)
    SUCCESS_STYLE = Style(color="green", bold=True)
    ERROR_STYLE = Style(color="red", bold=True)
    INFO_STYLE = Style(color="yellow")
    
    # Project type descriptions
    PROJECT_TYPES = [
        {
            "name": "React Frontend",
            "display": "⚛️  React Frontend",
            "description": "Modern React application with Vite",
            "value": "React Frontend"
        },
        {
            "name": "React + Supabase",
            "display": "⚡ React + Supabase",
            "description": "Full-stack React with Supabase backend",
            "value": "React + Supabase"
        },
        {
            "name": "Python Project",
            "display": "🐍 Python Project",
            "description": "Production-ready Python project structure",
            "value": "Python Project"
        }
    ]

    @staticmethod
    def print_header(text: str):
        """Print a styled header."""
        console.print()
        console.print(Panel(
            Text(text, style="bold blue", justify="center"),
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2)
        ))
        console.print()

    @staticmethod
    def print_success(text: str):
        """Print a success message."""
        console.print()
        console.print(Panel(
            Text(f"✨ {text} 🚀", style="bold green", justify="center"),
            box=box.ROUNDED,
            border_style="green",
            padding=(1, 2)
        ))
        console.print()

    @staticmethod
    def print_error(text: str):
        """Print an error message."""
        console.print()
        console.print(Panel(
            Text(f"❌ {text}", style="bold red", justify="center"),
            box=box.ROUNDED,
            border_style="red",
            padding=(1, 2)
        ))
        console.print()

    @staticmethod
    def print_info(text: str):
        """Print an info message."""
        console.print()
        console.print(Panel(
            Text(f"ℹ️  {text}", style="yellow", justify="center"),
            box=box.ROUNDED,
            border_style="yellow",
            padding=(1, 2)
        ))
        console.print()

    @classmethod
    def select_project_type(cls) -> str:
        """Prompt for project type selection."""
        console.print()
        console.print(Panel(
            Text("Select Project Type", style="bold blue", justify="center"),
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2)
        ))
        console.print()
        
        choices = [
            {
                "name": f"{project['display']}\n   {project['description']}",
                "value": project["value"]
            }
            for project in cls.PROJECT_TYPES
        ]
        
        return questionary.select(
            "Choose a template:",
            choices=choices,
            qmark="🎯",
            pointer="➜"
        ).ask()

    @staticmethod
    def get_project_name(default: str = None) -> str:
        """Prompt for project name."""
        console.print()
        console.print("📝 [bold]Project Configuration:[/bold]")
        console.print()
        
        return questionary.text(
            "Enter project name:",
            default=default or "",
            qmark="💡"
        ).ask()

    @staticmethod
    def select_features(project_type: str) -> List[str]:
        """Prompt for feature selection based on project type."""
        choices = []
        
        if project_type in ["React Frontend", "React + Supabase"]:
            choices = [
                {"name": "⚡ TypeScript", "value": "TypeScript", "checked": True},
                {"name": "🎨 Tailwind CSS", "value": "Tailwind CSS"},
                {"name": "🔍 ESLint", "value": "ESLint"},
                {"name": "✨ Prettier", "value": "Prettier"}
            ]
            
            if project_type == "React + Supabase":
                choices.extend([
                    {"name": "🔐 Authentication", "value": "Authentication"},
                    {"name": "📊 Database Helpers", "value": "Database Helpers"},
                    {"name": "📁 Storage Helpers", "value": "Storage Helpers"}
                ])
        
        elif project_type == "Python Project":
            choices = [
                {"name": "✨ Black", "value": "Black", "checked": True},
                {"name": "🔍 Flake8", "value": "Flake8", "checked": True},
                {"name": "🧪 pytest", "value": "pytest", "checked": True},
                {"name": "🔄 pre-commit hooks", "value": "pre-commit hooks"},
                {"name": "🐳 Docker setup", "value": "Docker setup"}
            ]
        
        if not choices:
            return []
        
        console.print()
        console.print(Panel(
            Text("Configure Features", style="bold blue", justify="center"),
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2)
        ))
        console.print()
        
        return questionary.checkbox(
            "Select features to include:",
            choices=choices,
            qmark="🛠️ ",
            pointer="➜"
        ).ask() or []

    @staticmethod
    def confirm(message: str) -> bool:
        """Prompt for confirmation."""
        console.print()
        return questionary.confirm(
            message,
            qmark="❓",
            default=False
        ).ask()
