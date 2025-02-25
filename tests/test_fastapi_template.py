"""Tests for FastAPI template."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess
from src.templates import FastAPITemplate

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path

@pytest.fixture
def template(temp_dir):
    """Create a FastAPI template instance."""
    return FastAPITemplate("test_project", [], temp_dir)

def test_basic_generation(template, temp_dir):
    """Test basic project generation without additional features."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Check directory structure
        assert (temp_dir / "src").exists()
        assert (temp_dir / "tests").exists()
        assert (temp_dir / "src" / "api").exists()
        assert (temp_dir / "src" / "core").exists()
        assert (temp_dir / "src" / "db").exists()
        assert (temp_dir / "src" / "models").exists()
        assert (temp_dir / "src" / "schemas").exists()
        assert (temp_dir / "src" / "services").exists()
        
        # Check main.py
        main_py = temp_dir / "src" / "main.py"
        assert main_py.exists()
        content = main_py.read_text()
        assert "from fastapi import FastAPI" in content
        assert "app = FastAPI" in content
        assert "CORSMiddleware" in content

def test_poetry_setup(temp_dir):
    """Test project generation with Poetry."""
    template = FastAPITemplate("test_project", ["Poetry"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify Poetry commands were called
        calls = [call[0][0] for call in mock_run.call_args_list]
        assert ["poetry", "init", "--no-interaction"] in calls
        assert any("poetry" in cmd and "add" in cmd for cmd in calls)

def test_requirements_setup(template, temp_dir):
    """Test requirements.txt generation."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Check requirements files
        requirements_txt = temp_dir / "requirements.txt"
        requirements_dev_txt = temp_dir / "requirements-dev.txt"
        
        assert requirements_txt.exists()
        assert requirements_dev_txt.exists()
        
        # Check content
        content = requirements_txt.read_text()
        assert "fastapi" in content
        assert "uvicorn" in content
        assert "pydantic" in content
        
        dev_content = requirements_dev_txt.read_text()
        assert "pytest" in dev_content
        assert "black" in dev_content
        assert "flake8" in dev_content

def test_sqlalchemy_setup(temp_dir):
    """Test project generation with SQLAlchemy."""
    template = FastAPITemplate("test_project", ["SQLAlchemy"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Check database setup
        db_file = temp_dir / "src" / "db" / "database.py"
        assert db_file.exists()
        content = db_file.read_text()
        assert "from sqlalchemy.ext.asyncio import create_async_engine" in content
        assert "class Base(DeclarativeBase):" in content
        
        # Check model setup
        model_file = temp_dir / "src" / "models" / "user.py"
        assert model_file.exists()
        content = model_file.read_text()
        assert "class User(Base):" in content

def test_alembic_setup(temp_dir):
    """Test project generation with Alembic."""
    template = FastAPITemplate("test_project", ["SQLAlchemy", "Alembic"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify Alembic initialization
        assert mock_run.call_args_list[0][0][0] == ["alembic", "init", "migrations"]
        
        # Check alembic.ini
        alembic_ini = temp_dir / "alembic.ini"
        assert alembic_ini.exists()
        content = alembic_ini.read_text()
        assert "[alembic]" in content
        assert "sqlalchemy.url" in content

def test_jwt_setup(temp_dir):
    """Test project generation with JWT authentication."""
    template = FastAPITemplate("test_project", ["JWT"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Check requirements
        requirements_txt = temp_dir / "requirements.txt"
        content = requirements_txt.read_text()
        assert "python-jose" in content
        assert "passlib" in content

def test_docker_setup(temp_dir):
    """Test project generation with Docker."""
    template = FastAPITemplate("test_project", ["Docker"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Check Docker files
        assert (temp_dir / "Dockerfile").exists()
        assert (temp_dir / "docker-compose.yml").exists()

def test_prometheus_setup(temp_dir):
    """Test project generation with Prometheus metrics."""
    template = FastAPITemplate("test_project", ["Prometheus"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Check requirements
        requirements_txt = temp_dir / "requirements.txt"
        content = requirements_txt.read_text()
        assert "prometheus-fastapi-instrumentator" in content

def test_api_docs_setup(temp_dir):
    """Test project generation with API documentation."""
    template = FastAPITemplate("test_project", ["API-Docs"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Check main.py for OpenAPI configuration
        main_py = temp_dir / "src" / "main.py"
        content = main_py.read_text()
        assert "title=" in content
        assert "description=" in content
        assert "version=" in content

def test_command_failure(template, temp_dir):
    """Test handling of command failures."""
    with patch.object(template, '_setup_requirements', return_value=False) as mock_setup:
        success = template.generate()
        assert not success
        
        # Check that the directory was cleaned up
        assert not temp_dir.exists()

def test_cleanup_on_exception(template, temp_dir):
    """Test cleanup when an exception occurs."""
    with patch.object(template, '_setup_requirements') as mock_setup:
        mock_setup.side_effect = Exception("Setup failed")
        
        success = template.generate()
        assert not success
        
        # Check that the directory was cleaned up
        assert not temp_dir.exists() 