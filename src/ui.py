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
            "display": "🔄 React Frontend",
            "description": "Modern React application (Next.js or Vite)",
            "value": "React Frontend"
        },
        {
            "name": "React + Supabase",
            "display": "🔄 React + Supabase",
            "description": "Full-stack React with Supabase backend",
            "value": "React + Supabase"
        },
        {
            "name": "T3 Stack",
            "display": "🚀 T3 Stack",
            "description": "Next.js + tRPC + Prisma + Tailwind + TypeScript",
            "value": "T3 Stack"
        },
        {
            "name": "FastAPI Backend",
            "display": "⏩ FastAPI Backend",
            "description": "Modern Python API with SQLAlchemy and auto-docs",
            "value": "FastAPI Backend"
        },
        {
            "name": "Express API",
            "display": "🛠️ Express API",
            "description": "TypeScript API with Prisma and Swagger",
            "value": "Express API"
        },
        {
            "name": "Python Project",
            "display": "🐍 Python Project",
            "description": "Production-ready Python project structure",
            "value": "Python Project"
        }
    ]

    # Framework choices for React
    REACT_FRAMEWORKS = [
        {
            "name": "📦 Next.js\n   Full-featured React framework with SSR and file-based routing",
            "value": "next"
        },
        {
            "name": "❗ Vite\n   Lightning fast, modern build tool for React SPAs",
            "value": "vite"
        }
    ]

    # Database choices
    DATABASE_TYPES = [
        {
            "name": "🐘 PostgreSQL\n   Robust, open-source relational database",
            "value": "postgres"
        },
        {
            "name": "📊 MongoDB\n   Flexible, document-based NoSQL database",
            "value": "mongodb"
        },
        {
            "name": "🔲 SQLite\n   Lightweight, file-based database",
            "value": "sqlite"
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
        console.print(Panel(
            Text("Project Configuration", style="bold blue", justify="center"),
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2)
        ))
        console.print()
        
        return questionary.text(
            "Enter project name:",
            default=default or "",
            qmark="💡"
        ).ask()

    @classmethod
    def select_react_framework(cls) -> str:
        """Prompt for React framework selection."""
        console.print()
        console.print(Panel(
            Text("Select Framework", style="bold blue", justify="center"),
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2)
        ))
        console.print()
        
        return questionary.select(
            "Choose a framework:",
            choices=cls.REACT_FRAMEWORKS,
            qmark="📦",
            pointer="➜"
        ).ask()

    @classmethod
    def select_features(cls, project_type: str, framework: str = None) -> List[str]:
        """Prompt for feature selection based on project type."""
        choices = []
        
        if project_type in ["React Frontend", "React + Supabase"]:
            # Base React features
            choices = [
                {"name": "⚡ TypeScript", "value": "TypeScript", "checked": True},
                {"name": "🎨 Tailwind CSS", "value": "Tailwind CSS"},
                {"name": "🔍 ESLint", "value": "ESLint"},
                {"name": "✨ Prettier", "value": "Prettier"}
            ]

            # Next.js specific features
            if framework == "next":
                choices.extend([
                    {"name": "📱 PWA Support", "value": "PWA"},
                    {"name": "🔄 API Routes", "value": "API Routes"},
                    {"name": "📊 MongoDB (with Prisma)", "value": "MongoDB"}
                ])
            
            # Supabase specific features
            if project_type == "React + Supabase":
                choices.extend([
                    {"name": "🔐 Authentication", "value": "Authentication"},
                    {"name": "📊 Database Helpers", "value": "Database Helpers"},
                    {"name": "📁 Storage Helpers", "value": "Storage Helpers"}
                ])

        elif project_type == "T3 Stack":
            choices = [
                {"name": "🔐 NextAuth.js", "value": "NextAuth", "checked": True},
                {"name": "📊 Prisma", "value": "Prisma", "checked": True},
                {"name": "🎨 Tailwind CSS", "value": "Tailwind CSS", "checked": True},
                {"name": "🔍 ESLint", "value": "ESLint", "checked": True},
                {"name": "✨ Prettier", "value": "Prettier", "checked": True},
                {"name": "📱 PWA Support", "value": "PWA"},
                {"name": "🎭 Jest Testing", "value": "Jest"},
                {"name": "🎮 tRPC Subscriptions", "value": "tRPC-Sub"},
                {"name": "📈 Prisma Studio UI", "value": "Prisma-Studio"}
            ]

        elif project_type == "FastAPI Backend":
            choices = [
                {"name": "🔐 JWT Authentication", "value": "JWT", "checked": True},
                {"name": "📊 SQLAlchemy ORM", "value": "SQLAlchemy", "checked": True},
                {"name": "📝 Pydantic Models", "value": "Pydantic", "checked": True},
                {"name": "🧪 pytest", "value": "pytest", "checked": True},
                {"name": "🔍 Black + Flake8", "value": "Linting", "checked": True},
                {"name": "📦 Poetry", "value": "Poetry"},
                {"name": "🐳 Docker", "value": "Docker"},
                {"name": "🔄 Alembic Migrations", "value": "Alembic"},
                {"name": "📈 Prometheus Metrics", "value": "Prometheus"},
                {"name": "📝 API Documentation", "value": "API-Docs"}
            ]

        elif project_type == "Express API":
            choices = [
                {"name": "⚡ TypeScript", "value": "TypeScript", "checked": True},
                {"name": "📊 Prisma ORM", "value": "Prisma", "checked": True},
                {"name": "🔐 JWT Auth", "value": "JWT", "checked": True},
                {"name": "📝 OpenAPI/Swagger", "value": "OpenAPI", "checked": True},
                {"name": "🧪 Jest Testing", "value": "Jest", "checked": True},
                {"name": "🔍 ESLint", "value": "ESLint", "checked": True},
                {"name": "✨ Prettier", "value": "Prettier", "checked": True},
                {"name": "🐳 Docker", "value": "Docker"},
                {"name": "📈 Prometheus Metrics", "value": "Prometheus"},
                {"name": "🔄 Rate Limiting", "value": "Rate-Limit"}
            ]
        
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
