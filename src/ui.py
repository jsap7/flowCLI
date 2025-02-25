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
    HEADER_STYLE = Style(color="cyan", bold=True)
    SUCCESS_STYLE = Style(color="green", bold=True)
    ERROR_STYLE = Style(color="red", bold=True)
    INFO_STYLE = Style(color="yellow")
    
    # Project Categories
    PROJECT_CATEGORIES = [
        {
            "name": "Web Development",
            "display": "🌐 Web Development",
            "description": "Frontend, Backend, and Full-stack web applications",
            "value": "web"
        },
        {
            "name": "Mobile Development",
            "display": "📱 Mobile Development",
            "description": "iOS, Android, and cross-platform mobile apps",
            "value": "mobile"
        },
        {
            "name": "Game Development",
            "display": "🎮 Game Development",
            "description": "2D, 3D, and browser-based games",
            "value": "game"
        },
        {
            "name": "Desktop Applications",
            "display": "🖥️ Desktop Applications",
            "description": "Cross-platform desktop apps and utilities",
            "value": "desktop"
        },
        {
            "name": "CLI & Scripts",
            "display": "⌨️ CLI & Scripts",
            "description": "Command-line tools, scripts, and automation",
            "value": "cli"
        },
        {
            "name": "Data & ML",
            "display": "🤖 Data & ML",
            "description": "Data science, ML, and AI applications",
            "value": "data"
        },
        {
            "name": "DevOps & Cloud",
            "display": "☁️ DevOps & Cloud",
            "description": "Infrastructure, deployment, and cloud services",
            "value": "devops"
        }
    ]
    
    # Project Templates by Category
    PROJECT_TEMPLATES = {
        "web": [
            {
                "name": "React Frontend",
                "display": "⚛️ React Frontend",
                "description": "Modern React application (Next.js or Vite)",
                "value": "React Frontend"
            },
            {
                "name": "T3 Stack",
                "display": "🚀 T3 Stack",
                "description": "Next.js + tRPC + Prisma + Tailwind + TypeScript",
                "value": "T3 Stack"
            },
            {
                "name": "React + Supabase",
                "display": "⚡ React + Supabase",
                "description": "Full-stack React with Supabase backend",
                "value": "React + Supabase"
            },
            {
                "name": "FastAPI Backend",
                "display": "⚡ FastAPI Backend",
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
                "name": "Vue Frontend",
                "display": "🟩 Vue Frontend",
                "description": "Vue 3 with Composition API and Vite",
                "value": "Vue Frontend"
            },
            {
                "name": "Django Full-stack",
                "display": "🎸 Django Full-stack",
                "description": "Python web framework with batteries included",
                "value": "Django Full-stack"
            }
        ],
        "mobile": [
            {
                "name": "React Native",
                "display": "📱 React Native",
                "description": "Cross-platform mobile apps with React Native",
                "value": "React Native"
            },
            {
                "name": "Flutter",
                "display": "🦋 Flutter",
                "description": "Cross-platform apps with Flutter and Dart",
                "value": "Flutter"
            },
            {
                "name": "Ionic React",
                "display": "⚡ Ionic React",
                "description": "Hybrid mobile apps with Ionic and React",
                "value": "Ionic React"
            }
        ],
        "game": [
            {
                "name": "Unity 2D",
                "display": "🎮 Unity 2D",
                "description": "2D game development with Unity and C#",
                "value": "Unity 2D"
            },
            {
                "name": "Godot",
                "display": "🎲 Godot",
                "description": "Open-source game engine with GDScript",
                "value": "Godot"
            },
            {
                "name": "Phaser",
                "display": "🌟 Phaser",
                "description": "HTML5 game framework with TypeScript",
                "value": "Phaser"
            },
            {
                "name": "PyGame",
                "display": "🐍 PyGame",
                "description": "Python game development with Pygame",
                "value": "PyGame"
            }
        ],
        "desktop": [
            {
                "name": "Electron",
                "display": "⚛️ Electron",
                "description": "Cross-platform desktop apps with JavaScript",
                "value": "Electron"
            },
            {
                "name": "Tauri",
                "display": "🦀 Tauri",
                "description": "Lightweight desktop apps with Rust",
                "value": "Tauri"
            },
            {
                "name": "PyQt",
                "display": "🐍 PyQt",
                "description": "Python desktop apps with Qt framework",
                "value": "PyQt"
            }
        ],
        "cli": [
            {
                "name": "Python CLI",
                "display": "🐍 Python CLI",
                "description": "Command-line tools with Typer/Click",
                "value": "Python CLI"
            },
            {
                "name": "Bash Script",
                "display": "📜 Bash Script",
                "description": "Shell scripts with best practices",
                "value": "Bash Script"
            },
            {
                "name": "Node CLI",
                "display": "📦 Node CLI",
                "description": "Command-line tools with Node.js",
                "value": "Node CLI"
            }
        ],
        "data": [
            {
                "name": "Data Science",
                "display": "📊 Data Science",
                "description": "Python data analysis with Pandas/NumPy",
                "value": "Data Science"
            },
            {
                "name": "ML Project",
                "display": "🧠 ML Project",
                "description": "Machine learning with PyTorch/TensorFlow",
                "value": "ML Project"
            },
            {
                "name": "FastAI",
                "display": "🚀 FastAI",
                "description": "Deep learning with fast.ai",
                "value": "FastAI"
            }
        ],
        "devops": [
            {
                "name": "Docker Compose",
                "display": "🐳 Docker Compose",
                "description": "Multi-container Docker applications",
                "value": "Docker Compose"
            },
            {
                "name": "K8s Template",
                "display": "☸️ K8s Template",
                "description": "Kubernetes deployment templates",
                "value": "K8s Template"
            },
            {
                "name": "Terraform",
                "display": "🏗️ Terraform",
                "description": "Infrastructure as Code with Terraform",
                "value": "Terraform"
            }
        ]
    }

    # Framework choices for React
    REACT_FRAMEWORKS = [
        {
            "name": "📦 Next.js\n   Full-featured React framework with SSR and file-based routing",
            "value": "next"
        },
        {
            "name": "⚡ Vite\n   Lightning fast, modern build tool for React SPAs",
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
            Text(text, style="cyan bold", justify="center"),
            box=box.HEAVY,
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()

    @staticmethod
    def print_success(text: str):
        """Print a success message."""
        console.print()
        console.print(Panel(
            Text(f"✨ {text} 🚀", style="green bold", justify="center"),
            box=box.HEAVY,
            border_style="green",
            padding=(1, 2)
        ))
        console.print()

    @staticmethod
    def print_error(text: str):
        """Print an error message."""
        console.print()
        console.print(Panel(
            Text(f"❌ {text}", style="red bold", justify="center"),
            box=box.HEAVY,
            border_style="red",
            padding=(1, 2)
        ))
        console.print()

    @staticmethod
    def print_info(text: str):
        """Print an info message."""
        console.print()
        console.print(Panel(
            Text(f"ℹ️  {text}", style="yellow bold", justify="center"),
            box=box.HEAVY,
            border_style="yellow",
            padding=(1, 2)
        ))
        console.print()

    @classmethod
    def select_category(cls) -> str:
        """Prompt for project category selection."""
        console.print()
        console.print(Panel(
            Text("Select Project Category", style="cyan bold", justify="center"),
            box=box.HEAVY,
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()
        
        choices = []
        for category in cls.PROJECT_CATEGORIES:
            # Add a separator before each category except the first one
            if choices:
                choices.append({"name": "─" * 50, "value": None, "disabled": True})
            
            description = Text()
            description.append(f"\n   {category['description']}", style="dim")
            
            choices.append({
                "name": f"{category['display']}{description}",
                "value": category["value"]
            })
        
        return questionary.select(
            "Choose a category:",
            choices=choices,
            qmark="📂",
            pointer="➜",
            style=questionary.Style([
                ('qmark', 'fg:cyan bold'),
                ('question', 'fg:white bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green bold'),
                ('separator', 'fg:grey'),
                ('disabled', 'fg:grey')
            ])
        ).ask()

    @classmethod
    def select_project_type(cls, category: str) -> str:
        """Prompt for project type selection within a category."""
        console.print()
        console.print(Panel(
            Text("Select Project Type", style="cyan bold", justify="center"),
            box=box.HEAVY,
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()
        
        choices = []
        templates = cls.PROJECT_TEMPLATES.get(category, [])
        
        # Group templates by type
        frontend_templates = []
        backend_templates = []
        fullstack_templates = []
        
        for template in templates:
            if "Frontend" in template["name"]:
                frontend_templates.append(template)
            elif "Backend" in template["name"] or "API" in template["name"]:
                backend_templates.append(template)
            else:
                fullstack_templates.append(template)
        
        # Add Frontend templates
        if frontend_templates:
            if choices:
                choices.append({"name": "─" * 50, "value": None, "disabled": True})
            choices.append({"name": "📱 Frontend", "value": None, "disabled": True})
            for template in frontend_templates:
                description = Text()
                description.append(f"\n   {template['description']}", style="dim")
                choices.append({
                    "name": f"{template['display']}{description}",
                    "value": template["value"]
                })
        
        # Add Backend templates
        if backend_templates:
            if choices:
                choices.append({"name": "─" * 50, "value": None, "disabled": True})
            choices.append({"name": "⚙️  Backend", "value": None, "disabled": True})
            for template in backend_templates:
                description = Text()
                description.append(f"\n   {template['description']}", style="dim")
                choices.append({
                    "name": f"{template['display']}{description}",
                    "value": template["value"]
                })
        
        # Add Full-stack templates
        if fullstack_templates:
            if choices:
                choices.append({"name": "─" * 50, "value": None, "disabled": True})
            choices.append({"name": "🎯 Full-stack", "value": None, "disabled": True})
            for template in fullstack_templates:
                description = Text()
                description.append(f"\n   {template['description']}", style="dim")
                choices.append({
                    "name": f"{template['display']}{description}",
                    "value": template["value"]
                })
        
        return questionary.select(
            "Choose a template:",
            choices=choices,
            qmark="🎯",
            pointer="➜",
            style=questionary.Style([
                ('qmark', 'fg:cyan bold'),
                ('question', 'fg:white bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green bold'),
                ('separator', 'fg:grey'),
                ('disabled', 'fg:grey')
            ])
        ).ask()

    @staticmethod
    def get_project_name(default: str = None) -> str:
        """Prompt for project name."""
        console.print()
        console.print(Panel(
            Text("Project Configuration", style="cyan bold", justify="center"),
            box=box.HEAVY,
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()
        
        return questionary.text(
            "Enter project name:",
            default=default or "",
            qmark="💡",
            style=questionary.Style([
                ('qmark', 'fg:cyan bold'),
                ('question', 'fg:white bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green bold')
            ])
        ).ask()

    @classmethod
    def select_react_framework(cls) -> str:
        """Prompt for React framework selection."""
        console.print()
        console.print(Panel(
            Text("Select Framework", style="cyan bold", justify="center"),
            box=box.HEAVY,
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()
        
        return questionary.select(
            "Choose a framework:",
            choices=cls.REACT_FRAMEWORKS,
            qmark="📦",
            pointer="➜",
            style=questionary.Style([
                ('qmark', 'fg:cyan bold'),
                ('question', 'fg:white bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green bold'),
                ('separator', 'fg:grey'),
                ('disabled', 'fg:grey')
            ])
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

        elif project_type == "Vue Frontend":
            choices = [
                {"name": "⚡ TypeScript", "value": "TypeScript", "checked": True},
                {"name": "🎨 Tailwind CSS", "value": "Tailwind CSS"},
                {"name": "🔍 ESLint", "value": "ESLint"},
                {"name": "✨ Prettier", "value": "Prettier"},
                {"name": "🛣️ Vue Router", "value": "Vue Router"},
                {"name": "📦 Pinia (State Management)", "value": "Pinia"},
                {"name": "🧪 Vitest", "value": "Vitest"},
                {"name": "🔄 Cypress", "value": "Cypress"},
                {"name": "📱 PWA Support", "value": "PWA"},
                {"name": "🌐 i18n", "value": "i18n"},
                {"name": "⚛️ JSX", "value": "JSX"}
            ]

        elif project_type == "Django Full-stack":
            choices = [
                {"name": "🐘 PostgreSQL", "value": "PostgreSQL"},
                {"name": "🎲 MySQL", "value": "MySQL"},
                {"name": "🔐 Authentication", "value": "Authentication"},
                {"name": "🚀 DRF (Django REST Framework)", "value": "DRF"},
                {"name": "📝 API Docs (drf-spectacular)", "value": "API Docs"},
                {"name": "🔄 CORS Headers", "value": "CORS"},
                {"name": "🐞 Debug Toolbar", "value": "Debug Toolbar"},
                {"name": "🔧 Django Extensions", "value": "Django Extensions"},
                {"name": "📦 Celery", "value": "Celery"},
                {"name": "📊 Redis", "value": "Redis"},
                {"name": "🐳 Docker", "value": "Docker"},
                {"name": "🧪 Testing", "value": "Testing"},
                {"name": "📄 WhiteNoise", "value": "WhiteNoise"},
                {"name": "🚀 Production Ready", "value": "Production"}
            ]

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
            Text("Configure Features", style="cyan bold", justify="center"),
            box=box.HEAVY,
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()
        
        return questionary.checkbox(
            "Select features to include:",
            choices=choices,
            qmark="🛠️ ",
            pointer="➜",
            style=questionary.Style([
                ('qmark', 'fg:cyan bold'),
                ('question', 'fg:white bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green bold'),
                ('separator', 'fg:grey'),
                ('disabled', 'fg:grey')
            ])
        ).ask() or []

    @staticmethod
    def confirm(message: str) -> bool:
        """Prompt for confirmation."""
        console.print()
        return questionary.confirm(
            message,
            qmark="❓",
            default=False,
            style=questionary.Style([
                ('qmark', 'fg:cyan bold'),
                ('question', 'fg:white bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green bold')
            ])
        ).ask()
