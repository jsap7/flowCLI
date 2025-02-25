import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from src.templates.react_supabase import ReactSupabaseTemplate

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

def test_basic_generation(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        template = ReactSupabaseTemplate("test-project", [], temp_dir)
        
        assert template.generate() is True
        
        # Verify React base setup was called
        assert any('create' in str(call) and 'vite' in str(call) for call in mock_run.call_args_list)
        
        # Verify Supabase client installation
        npm_install_calls = [list(call[0][0]) for call in mock_run.call_args_list]
        assert ['npm', 'install', '@supabase/supabase-js'] in npm_install_calls
        
        # Verify Supabase client files were created
        assert mock_write.call_count > 0
        
        # Get written content
        written_content = [str(call[0][0]) for call in mock_write.call_args_list]
        assert any('VITE_SUPABASE_URL' in content for content in written_content)
        assert any('createClient' in content for content in written_content)

def test_auth_setup(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        template = ReactSupabaseTemplate("test-project", ["Authentication"], temp_dir)
        
        assert template.generate() is True
        
        # Verify auth context file was created
        assert mock_write.call_count > 0
        
        # Get written content
        written_content = [str(call[0][0]) for call in mock_write.call_args_list]
        assert any('AuthContext' in content for content in written_content)
        assert any('AuthProvider' in content for content in written_content)
        assert any('signInWithPassword' in content for content in written_content)

def test_database_helpers_setup(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        template = ReactSupabaseTemplate("test-project", ["Database Helpers"], temp_dir)
        
        assert template.generate() is True
        
        # Verify database helper functions were created
        assert mock_write.call_count > 0
        
        # Get written content
        written_content = [str(call[0][0]) for call in mock_write.call_args_list]
        assert any('fetchData' in content for content in written_content)
        assert any('insertData' in content for content in written_content)
        assert any('updateData' in content for content in written_content)
        assert any('deleteData' in content for content in written_content)

def test_storage_helpers_setup(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        template = ReactSupabaseTemplate("test-project", ["Storage Helpers"], temp_dir)
        
        assert template.generate() is True
        
        # Verify storage helper functions were created
        assert mock_write.call_count > 0
        
        # Get written content
        written_content = [str(call[0][0]) for call in mock_write.call_args_list]
        assert any('uploadFile' in content for content in written_content)
        assert any('downloadFile' in content for content in written_content)
        assert any('deleteFile' in content for content in written_content)
        assert any('getPublicUrl' in content for content in written_content)

def test_multiple_features(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        template = ReactSupabaseTemplate("test-project", [
            "Authentication",
            "Database Helpers",
            "Storage Helpers"
        ], temp_dir)
        
        assert template.generate() is True
        
        # Verify all feature files were created
        assert mock_write.call_count > 0
        
        # Get written content
        written_content = [str(call[0][0]) for call in mock_write.call_args_list]
        assert any('AuthContext' in content for content in written_content)
        assert any('fetchData' in content for content in written_content)
        assert any('uploadFile' in content for content in written_content)

def test_npm_install_failure(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        def mock_run_side_effect(args, **kwargs):
            if '@supabase/supabase-js' in args:
                result = MagicMock()
                result.returncode = 1
                return result
            result = MagicMock()
            result.returncode = 0
            return result
            
        mock_run.side_effect = mock_run_side_effect
        template = ReactSupabaseTemplate("test-project", [], temp_dir)
        
        assert template.generate() is False

def test_file_write_error(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        mock_write.side_effect = PermissionError()
        
        template = ReactSupabaseTemplate("test-project", [], temp_dir)
        assert template.generate() is False

def test_base_template_generation_failure(temp_dir):
    with patch('src.templates.react.ReactTemplate.generate') as mock_generate:
        mock_generate.return_value = False
        template = ReactSupabaseTemplate("test-project", [], temp_dir)
        assert template.generate() is False

def test_supabase_client_setup_error(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        mock_write.side_effect = [None, PermissionError()]  # Make second write fail
        
        template = ReactSupabaseTemplate("test-project", [], temp_dir)
        assert template.generate() is False

def test_auth_setup_error(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        mock_write.side_effect = [None, None, PermissionError()]  # Make auth file write fail
        
        template = ReactSupabaseTemplate("test-project", ["Authentication"], temp_dir)
        assert template.generate() is False

def test_database_helpers_setup_error(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        mock_write.side_effect = [None, None, PermissionError()]  # Make db helpers file write fail
        
        template = ReactSupabaseTemplate("test-project", ["Database Helpers"], temp_dir)
        assert template.generate() is False

def test_storage_helpers_setup_error(temp_dir):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_run.return_value.returncode = 0
        mock_write.side_effect = [None, None, PermissionError()]  # Make storage helpers file write fail
        
        template = ReactSupabaseTemplate("test-project", ["Storage Helpers"], temp_dir)
        assert template.generate() is False 