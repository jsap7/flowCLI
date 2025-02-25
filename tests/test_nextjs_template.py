"""Tests for Next.js template."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import subprocess
from src.templates import NextjsTemplate

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path

@pytest.fixture
def template(temp_dir):
    """Create a Next.js template instance."""
    return NextjsTemplate("test_project", [], temp_dir)

def test_basic_generation(template, temp_dir):
    """Test basic project generation without additional features."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify create-next-app command was called with correct arguments
        expected_cmd = [
            "npx",
            "create-next-app@latest",
            "test_project",
            "--js",  # No TypeScript
            "--no-tailwind",  # No Tailwind
            "--no-eslint",  # No ESLint
            "--app",  # Use App Router
            "--src-dir",  # Use src/ directory
            "--import-alias", "@/*",  # Modern import alias
            "--no-git",  # We'll handle git ourselves
        ]
        
        # Check if the command was called with the correct arguments
        actual_cmd = mock_run.call_args_list[0][0][0]
        assert actual_cmd == expected_cmd
        assert mock_run.call_args_list[0][1]['cwd'] == temp_dir.parent

def test_typescript_feature(temp_dir):
    """Test project generation with TypeScript."""
    template = NextjsTemplate("test_project", ["TypeScript"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify TypeScript flag was included
        cmd_args = mock_run.call_args_list[0][0][0]
        assert "--ts" in cmd_args

def test_tailwind_feature(temp_dir):
    """Test project generation with Tailwind CSS."""
    template = NextjsTemplate("test_project", ["Tailwind CSS"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify Tailwind flag was included
        cmd_args = mock_run.call_args_list[0][0][0]
        assert "--tailwind" in cmd_args

def test_eslint_feature(temp_dir):
    """Test project generation with ESLint."""
    template = NextjsTemplate("test_project", ["ESLint"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify ESLint flag was included
        cmd_args = mock_run.call_args_list[0][0][0]
        assert "--eslint" in cmd_args

def test_prettier_setup(temp_dir):
    """Test project generation with Prettier."""
    template = NextjsTemplate("test_project", ["Prettier"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.return_value = None
        
        success = template.generate()
        assert success
        
        # Verify Prettier dependencies were installed
        npm_install_cmd = mock_run.call_args_list[1][0][0]
        assert "prettier" in npm_install_cmd
        assert "prettier-plugin-tailwindcss" in npm_install_cmd
        assert "eslint-config-prettier" in npm_install_cmd
        
        # Verify config file was written
        write_calls = [call.args[0] for call in mock_write.call_args_list]
        assert any("semi" in content for content in write_calls)
        assert any("singleQuote" in content for content in write_calls)

def test_pwa_setup(temp_dir):
    """Test project generation with PWA."""
    template = NextjsTemplate("test_project", ["PWA"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.return_value = None
        
        success = template.generate()
        assert success
        
        # Verify PWA dependencies were installed
        npm_install_cmd = mock_run.call_args_list[1][0][0]
        assert "next-pwa" in npm_install_cmd
        
        # Verify config files were written
        write_calls = [call.args[0] for call in mock_write.call_args_list]
        assert any("withPWA" in content for content in write_calls)
        assert any('"name": "Your App"' in content for content in write_calls)

def test_mongodb_setup(temp_dir):
    """Test project generation with MongoDB."""
    template = NextjsTemplate("test_project", ["MongoDB"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.return_value = None
        
        success = template.generate()
        assert success
        
        # Verify MongoDB dependencies were installed
        npm_install_cmd = mock_run.call_args_list[1][0][0]
        assert "npm" in npm_install_cmd
        assert "install" in npm_install_cmd
        assert "-D" in npm_install_cmd
        assert "@prisma/client" in npm_install_cmd
        assert "prisma" in npm_install_cmd
        
        # Verify Prisma was initialized
        prisma_cmd = mock_run.call_args_list[2][0][0]
        assert prisma_cmd == ["npx", "prisma", "init"]
        
        # Verify config files were written
        write_calls = [call.args[0] for call in mock_write.call_args_list]
        assert any('provider = "mongodb"' in content for content in write_calls)
        assert any("PrismaClient" in content for content in write_calls)

def test_multiple_features(temp_dir):
    """Test project generation with multiple features."""
    features = ["TypeScript", "Tailwind CSS", "ESLint", "Prettier", "PWA", "MongoDB"]
    template = NextjsTemplate("test_project", features, temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.return_value = None
        
        success = template.generate()
        assert success
        
        # Verify create-next-app command includes all feature flags
        cmd_args = mock_run.call_args_list[0][0][0]
        assert "--ts" in cmd_args
        assert "--tailwind" in cmd_args
        assert "--eslint" in cmd_args
        
        # Verify all dependencies were installed
        npm_install_cmds = [call[0][0] for call in mock_run.call_args_list[1:]]
        installed_packages = [pkg for cmd in npm_install_cmds for pkg in cmd if isinstance(pkg, str)]
        
        assert "prettier" in installed_packages
        assert "next-pwa" in installed_packages
        assert "@prisma/client" in installed_packages
        
        # Verify all config files were written
        write_calls = [call.args[0] for call in mock_write.call_args_list]
        assert any("semi" in content for content in write_calls)  # Prettier config
        assert any("withPWA" in content for content in write_calls)  # PWA config
        assert any('provider = "mongodb"' in content for content in write_calls)  # Prisma config

def test_create_next_app_failure(template, temp_dir):
    """Test handling of create-next-app command failure."""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "create-next-app")
        
        success = template.generate()
        assert not success

def test_npm_install_failure(temp_dir):
    """Test handling of npm install failure."""
    template = NextjsTemplate("test_project", ["Prettier"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir:
        mock_run.return_value = MagicMock(returncode=0)
        mock_run.side_effect = [
            MagicMock(returncode=0),  # create-next-app succeeds
            subprocess.CalledProcessError(1, "npm install")  # npm install fails
        ]
        
        success = template.generate()
        assert not success

def test_prisma_init_failure(temp_dir):
    """Test handling of Prisma initialization failure."""
    template = NextjsTemplate("test_project", ["MongoDB"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir:
        mock_run.return_value = MagicMock(returncode=0)
        mock_run.side_effect = [
            MagicMock(returncode=0),  # create-next-app succeeds
            MagicMock(returncode=0),  # npm install succeeds
            subprocess.CalledProcessError(1, "prisma init")  # prisma init fails
        ]
        
        success = template.generate()
        assert not success

def test_file_write_error(temp_dir):
    """Test handling of file write errors."""
    template = NextjsTemplate("test_project", ["Prettier"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.side_effect = PermissionError("Permission denied")
        
        success = template.generate()
        assert not success 