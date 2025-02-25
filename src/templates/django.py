from pathlib import Path
from typing import List
from .base import BaseTemplate

class DjangoTemplate(BaseTemplate):
    def _create_directory(self, path: Path):
        """Create a directory if it doesn't exist."""
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise Exception(f"Failed to create directory {path}: {str(e)}")

    def generate(self):
        """Generate a Django project with modern best practices."""
        # Create target directory first
        self._create_directory(self.target_dir)
        
        # Create virtual environment
        success = self._run_command([
            "python",
            "-m",
            "venv",
            "venv"
        ], self.target_dir)
        
        if not success:
            return False
        
        # Get virtual environment paths
        venv_python = str(self.target_dir / "venv" / "bin" / "python")
        venv_pip = str(self.target_dir / "venv" / "bin" / "pip")
        
        # Install Django and base dependencies
        requirements = [
            "django>=5.0.0",
            "python-dotenv>=1.0.0",
            "django-environ>=0.11.0",
            "psycopg>=3.1.0" if "PostgreSQL" in self.features else "",
            "mysqlclient>=2.2.0" if "MySQL" in self.features else "",
            "django-debug-toolbar>=4.2.0" if "Debug Toolbar" in self.features else "",
            "django-cors-headers>=4.3.0" if "CORS" in self.features else "",
            "djangorestframework>=3.14.0" if "DRF" in self.features else "",
            "drf-spectacular>=0.27.0" if "API Docs" in self.features else "",
            "celery>=5.3.0" if "Celery" in self.features else "",
            "redis>=5.0.0" if "Redis" in self.features else "",
            "django-allauth>=0.60.0" if "Authentication" in self.features else "",
            "whitenoise>=6.6.0" if "WhiteNoise" in self.features else "",
            "gunicorn>=21.2.0" if "Production" in self.features else "",
        ]
        
        # Filter out empty strings and install requirements
        requirements = [req for req in requirements if req]
        success = self._run_command([venv_pip, "install", *requirements], self.target_dir)
        
        if not success:
            return False
        
        # Create Django project using the virtual environment's Python
        success = self._run_command([
            venv_python,
            "-m",
            "django",
            "startproject",
            "config",
            "."
        ], self.target_dir)
        
        if not success:
            return False
        
        # Create main app using the virtual environment's Python
        success = self._run_command([
            venv_python,
            "manage.py",
            "startapp",
            "core"
        ], self.target_dir)
        
        if not success:
            return False
        
        # Set up project structure
        self._setup_project_structure()
        
        # Set up environment variables
        self._setup_env()
        
        # Set up settings
        self._setup_settings()
        
        # Set up Docker if selected
        if "Docker" in self.features:
            self._setup_docker()
        
        # Set up testing
        if "Testing" in self.features:
            self._setup_testing()
        
        return True
    
    def _setup_project_structure(self):
        """Set up modern Django project structure."""
        # Create necessary directories
        dirs = [
            self.target_dir / "static",
            self.target_dir / "media",
            self.target_dir / "templates",
            self.target_dir / "core" / "templates" / "core",
            self.target_dir / "core" / "static" / "core",
        ]
        
        for dir_path in dirs:
            self._create_directory(dir_path)
        
        # Create base template
        base_template = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django App{% endblock %}</title>
    {% if debug %}
        <script src="https://cdn.tailwindcss.com"></script>
    {% else %}
        <link rel="stylesheet" href="{% static 'css/main.min.css' %}">
    {% endif %}
    {% block extra_css %}{% endblock %}
</head>
<body class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow">
        <!-- Add your navigation here -->
    </nav>

    <main class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>

    <footer class="bg-white shadow mt-8">
        <!-- Add your footer here -->
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
"""
        self._write_file(self.target_dir / "templates" / "base.html", base_template)
        
        # Create requirements files
        self._write_file(self.target_dir / "requirements.txt", "\n".join([
            "# Core dependencies",
            "django>=5.0.0",
            "python-dotenv>=1.0.0",
            "django-environ>=0.11.0",
            "",
            "# Database",
            "psycopg>=3.1.0" if "PostgreSQL" in self.features else "# Add your database driver here",
            "",
            "# Development",
            "django-debug-toolbar>=4.2.0" if "Debug Toolbar" in self.features else "# django-debug-toolbar",
            "",
            "# API",
            "djangorestframework>=3.14.0" if "DRF" in self.features else "# djangorestframework",
            "drf-spectacular>=0.27.0" if "API Docs" in self.features else "# drf-spectacular",
            "",
            "# Authentication",
            "django-allauth>=0.60.0" if "Authentication" in self.features else "# django-allauth",
            "",
            "# Production",
            "gunicorn>=21.2.0" if "Production" in self.features else "# gunicorn",
            "whitenoise>=6.6.0" if "WhiteNoise" in self.features else "# whitenoise",
            "",
            "# Task Queue",
            "celery>=5.3.0" if "Celery" in self.features else "# celery",
            "redis>=5.0.0" if "Redis" in self.features else "# redis",
        ]))
    
    def _setup_env(self):
        """Set up environment variables."""
        env_content = """# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3
"""
        
        if "PostgreSQL" in self.features:
            env_content += "# DATABASE_URL=postgres://user:password@localhost:5432/dbname\n"
        
        if "Redis" in self.features:
            env_content += "\n# Redis\nREDIS_URL=redis://localhost:6379/0\n"
        
        self._write_file(self.target_dir / ".env", env_content)
        self._write_file(self.target_dir / ".env.example", env_content)
    
    def _setup_settings(self):
        """Set up Django settings with best practices."""
        settings_path = self.target_dir / "config" / "settings.py"
        
        # Create config directory if it doesn't exist
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create settings.py with default content if it doesn't exist
        if not settings_path.exists():
            default_settings = '''"""
Django settings for config project.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-default'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
'''
            self._write_file(settings_path, default_settings)
        
        # Read existing settings
        current_settings = settings_path.read_text()
        
        # Add imports
        imports = """import os
from pathlib import Path
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
"""
        
        # Replace secret key
        new_settings = current_settings.replace(
            "SECRET_KEY = 'django-insecure-",
            "SECRET_KEY = env('SECRET_KEY')"
        )
        
        # Update debug and allowed hosts
        new_settings = new_settings.replace(
            "DEBUG = True",
            "DEBUG = env('DEBUG')"
        ).replace(
            "ALLOWED_HOSTS = []",
            "ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')"
        )
        
        # Add installed apps
        additional_apps = [
            "    'core.apps.CoreConfig',",
            "    'django_extensions'," if "Django Extensions" in self.features else "",
            "    'debug_toolbar'," if "Debug Toolbar" in self.features else "",
            "    'rest_framework'," if "DRF" in self.features else "",
            "    'drf_spectacular'," if "API Docs" in self.features else "",
            "    'corsheaders'," if "CORS" in self.features else "",
            "    'allauth'," if "Authentication" in self.features else "",
            "    'allauth.account'," if "Authentication" in self.features else "",
            "    'allauth.socialaccount'," if "Authentication" in self.features else "",
        ]
        
        # Filter out empty strings
        additional_apps = [app for app in additional_apps if app]
        
        # Add middleware
        additional_middleware = [
            "    'debug_toolbar.middleware.DebugToolbarMiddleware'," if "Debug Toolbar" in self.features else "",
            "    'corsheaders.middleware.CorsMiddleware'," if "CORS" in self.features else "",
            "    'whitenoise.middleware.WhiteNoiseMiddleware'," if "WhiteNoise" in self.features else "",
        ]
        
        # Filter out empty strings
        additional_middleware = [mw for mw in additional_middleware if mw]
        
        # Write updated settings
        self._write_file(settings_path, new_settings)
    
    def _setup_docker(self):
        """Set up Docker configuration."""
        # Create Dockerfile
        dockerfile = """FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run the application
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
"""
        self._write_file(self.target_dir / "Dockerfile", dockerfile)
        
        # Create docker-compose.yml
        compose = """version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
"""
        
        if "PostgreSQL" in self.features:
            compose += """
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=django
      - POSTGRES_USER=django
      - POSTGRES_PASSWORD=django

volumes:
  postgres_data:
"""
        
        if "Redis" in self.features:
            compose += """
  redis:
    image: redis:7
    ports:
      - "6379:6379"
"""
        
        self._write_file(self.target_dir / "docker-compose.yml", compose)
    
    def _setup_testing(self):
        """Set up testing configuration."""
        # Install test dependencies
        pip_cmd = str(self.target_dir / "venv" / "bin" / "pip")
        self._run_command([
            pip_cmd,
            "install",
            "pytest-django",
            "pytest-cov",
            "factory-boy"
        ])
        
        # Create pytest.ini
        pytest_ini = """[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
addopts = --nomigrations --cov=. --cov-report=html
"""
        self._write_file(self.target_dir / "pytest.ini", pytest_ini)
        
        # Create test directory
        test_dir = self.target_dir / "core" / "tests"
        self._create_directory(test_dir)
        
        # Create example test
        test_content = """import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_homepage_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
"""
        self._write_file(test_dir / "test_views.py", test_content) 