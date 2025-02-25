"""Tests for T3 template."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import subprocess
from src.templates import T3Template

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path

@pytest.fixture
def template(temp_dir):
    """Create a T3 template instance."""
    return T3Template("test_project", [], temp_dir)

def test_basic_generation(template, temp_dir):
    """Test basic project generation without additional features."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify create-t3-app command was called with correct arguments
        expected_cmd = [
            "npx",
            "create-t3-app@latest",
            "test_project",
            "--noGit",
            "--CI",
            "--tailwind", "true",
            "--trpc", "true",
            "--appRouter", "true"
        ]
        
        # Check if the command was called with the correct arguments
        actual_cmd = mock_run.call_args_list[0][0][0]
        assert actual_cmd == expected_cmd
        assert mock_run.call_args_list[0][1]['cwd'] == temp_dir.parent

def test_nextauth_feature(temp_dir):
    """Test project generation with NextAuth feature."""
    template = T3Template("test_project", ["NextAuth"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify NextAuth flag was included
        cmd_args = mock_run.call_args_list[0][0][0]
        assert "--nextAuth" in cmd_args
        assert "true" in cmd_args

def test_prisma_feature(temp_dir):
    """Test project generation with Prisma feature."""
    template = T3Template("test_project", ["Prisma"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        success = template.generate()
        assert success
        
        # Verify Prisma flag was included
        cmd_args = mock_run.call_args_list[0][0][0]
        assert "--prisma" in cmd_args
        assert "true" in cmd_args

def test_pwa_setup(temp_dir):
    """Test project generation with PWA feature."""
    template = T3Template("test_project", ["PWA"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.return_value = None  # write_text returns None
        
        success = template.generate()
        assert success
        
        # Verify PWA dependencies were installed
        npm_install_cmd = mock_run.call_args_list[1][0][0]
        assert "next-pwa" in npm_install_cmd
        
        # Verify directories were created
        mock_mkdir.assert_called()
        
        # Verify files were written with correct content
        write_calls = [call.args[0] for call in mock_write.call_args_list]
        assert any("withPWA" in content for content in write_calls)
        assert any('"name": "T3 App"' in content for content in write_calls)

def test_jest_setup(temp_dir):
    """Test project generation with Jest feature."""
    template = T3Template("test_project", ["Jest"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.return_value = None  # write_text returns None
        
        success = template.generate()
        assert success
        
        # Verify Jest dependencies were installed
        npm_install_cmd = mock_run.call_args_list[1][0][0]
        assert "@testing-library/react" in npm_install_cmd
        assert "jest" in npm_install_cmd
        assert "ts-jest" in npm_install_cmd
        
        # Verify directories were created
        mock_mkdir.assert_called()
        
        # Verify files were written with correct content
        write_calls = [call.args[0] for call in mock_write.call_args_list]
        assert any("preset: 'ts-jest'" in content for content in write_calls)
        assert any("@testing-library/jest-dom" in content for content in write_calls)

def test_trpc_subscriptions_setup(temp_dir):
    """Test project generation with tRPC subscriptions feature."""
    template = T3Template("test_project", ["tRPC-Sub"], temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.return_value = None  # write_text returns None
        
        success = template.generate()
        assert success
        
        # Verify tRPC subscription dependencies were installed
        npm_install_cmd = mock_run.call_args_list[1][0][0]
        assert "@trpc/server" in npm_install_cmd
        assert "@trpc/client" in npm_install_cmd
        assert "ws" in npm_install_cmd
        
        # Verify directories were created
        mock_mkdir.assert_called()
        
        # Verify files were written with correct content
        write_calls = [call.args[0] for call in mock_write.call_args_list]
        assert any("createWSClient" in content for content in write_calls)
        assert any("wsLink" in content for content in write_calls)

def test_multiple_features(temp_dir):
    """Test project generation with multiple features."""
    features = ["NextAuth", "Prisma", "PWA", "Jest", "tRPC-Sub"]
    template = T3Template("test_project", features, temp_dir)
    
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        mock_run.return_value = MagicMock(returncode=0)
        mock_write.return_value = None  # write_text returns None
        
        success = template.generate()
        assert success
        
        # Verify create-t3-app command includes all feature flags
        cmd_args = mock_run.call_args_list[0][0][0]
        assert "--nextAuth" in cmd_args
        assert "--prisma" in cmd_args
        
        # Verify all dependencies were installed
        npm_install_cmds = [call[0][0] for call in mock_run.call_args_list[1:]]
        installed_packages = [pkg for cmd in npm_install_cmds for pkg in cmd if isinstance(pkg, str)]
        
        assert "next-pwa" in installed_packages
        assert "@testing-library/react" in installed_packages
        assert "@trpc/server" in installed_packages
        
        # Verify directories were created
        mock_mkdir.assert_called()
        
        # Verify files were written with correct content
        write_calls = [call.args[0] for call in mock_write.call_args_list]
        assert any("withPWA" in content for content in write_calls)
        assert any("preset: 'ts-jest'" in content for content in write_calls)
        assert any("createWSClient" in content for content in write_calls)

def test_create_t3_app_failure(template, temp_dir):
    """Test handling of create-t3-app command failure."""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "create-t3-app")
        
        success = template.generate()
        assert not success

def test_npm_install_failure(temp_dir):
    """Test handling of npm install failure."""
    template = T3Template("test_project", ["PWA"], temp_dir)
    
    with patch('subprocess.run') as mock_run:
        def mock_run_with_npm_failure(cmd, *args, **kwargs):
            if "npm" in cmd:
                raise subprocess.CalledProcessError(1, cmd)
            return MagicMock(returncode=0)
        
        mock_run.side_effect = mock_run_with_npm_failure
        
        success = template.generate()
        assert not success

def test_file_write_error(template, temp_dir):
    """Test handling of file write errors."""
    with patch('pathlib.Path.write_text') as mock_write:
        mock_write.side_effect = PermissionError("Permission denied")
        
        success = template.generate()
        assert not success 