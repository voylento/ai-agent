import unittest
import tempfile
import os
from pathlib import Path

from functions.get_files_info import (
        is_directory_allowed,
    )

class TestIsDirectoryAllowed(unittest.TestCase):
    
    def setUp(self):
        """Set up temporary directories for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.working_dir = Path(self.temp_dir) / "working"
        self.working_dir.mkdir()
        
        # Create subdirectories
        self.subdir = self.working_dir / "subdir"
        self.subdir.mkdir()
        
        self.nested_subdir = self.subdir / "nested"
        self.nested_subdir.mkdir()
        
        # Create sibling directory
        self.sibling_dir = Path(self.temp_dir) / "sibling"
        self.sibling_dir.mkdir()
        
        # Create parent directory structure
        self.parent_dir = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up temporary directories"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_same_directory(self):
        """Test that the working directory itself is allowed"""
        self.assertTrue(is_directory_allowed(self.working_dir, self.working_dir))
    
    def test_direct_subdirectory(self):
        """Test that a direct subdirectory is allowed"""
        self.assertTrue(is_directory_allowed(self.working_dir, self.subdir))
    
    def test_nested_subdirectory(self):
        """Test that a nested subdirectory is allowed"""
        self.assertTrue(is_directory_allowed(self.working_dir, self.nested_subdir))
    
    def test_parent_directory_denied(self):
        """Test that parent directory is denied"""
        self.assertFalse(is_directory_allowed(self.working_dir, self.parent_dir))
    
    def test_sibling_directory_denied(self):
        """Test that sibling directory is denied"""
        self.assertFalse(is_directory_allowed(self.working_dir, self.sibling_dir))
    
    def test_nonexistent_directory_denied(self):
        """Test that non-existent directories are denied"""
        nonexistent = self.working_dir / "nonexistent"
        self.assertFalse(is_directory_allowed(self.working_dir, nonexistent))
    
    def test_nonexistent_outside_directory_denied(self):
        """Test that non-existent directories outside working dir are denied"""
        nonexistent = self.parent_dir / "nonexistent"
        self.assertFalse(is_directory_allowed(self.working_dir, nonexistent))
    
    def test_relative_paths_same_directory(self):
        """Test using relative paths for same directory"""
        old_cwd = os.getcwd()
        try:
            os.chdir(self.working_dir)
            self.assertTrue(is_directory_allowed(".", "."))
        finally:
            os.chdir(old_cwd)
    
    def test_relative_paths_subdirectory(self):
        """Test using relative paths for subdirectory"""
        old_cwd = os.getcwd()
        try:
            os.chdir(self.working_dir)
            self.assertTrue(is_directory_allowed(".", "subdir"))
        finally:
            os.chdir(old_cwd)
    
    def test_relative_paths_parent_denied(self):
        """Test using relative paths to access parent directory"""
        old_cwd = os.getcwd()
        try:
            os.chdir(self.working_dir)
            self.assertFalse(is_directory_allowed(".", ".."))
        finally:
            os.chdir(old_cwd)
    
    def test_mixed_path_types(self):
        """Test mixing absolute and relative paths"""
        old_cwd = os.getcwd()
        try:
            os.chdir(self.working_dir)
            # Absolute working dir, relative user dir
            self.assertTrue(is_directory_allowed(str(self.working_dir), "subdir"))
            # Relative working dir, absolute user dir
            self.assertTrue(is_directory_allowed(".", str(self.subdir)))
        finally:
            os.chdir(old_cwd)
    
    def test_string_paths(self):
        """Test that string paths work correctly"""
        self.assertTrue(is_directory_allowed(str(self.working_dir), str(self.subdir)))
        self.assertFalse(is_directory_allowed(str(self.working_dir), str(self.sibling_dir)))
    
    def test_path_objects(self):
        """Test that Path objects work correctly"""
        self.assertTrue(is_directory_allowed(self.working_dir, self.subdir))
        self.assertFalse(is_directory_allowed(self.working_dir, self.sibling_dir))
    
    def test_symlink_handling(self):
        """Test handling of symbolic links"""
        # Create a symlink inside working directory pointing to sibling
        symlink_path = self.working_dir / "symlink_to_sibling"
        try:
            symlink_path.symlink_to(self.sibling_dir)
            # Symlink should be denied because it resolves to outside working dir
            self.assertFalse(is_directory_allowed(self.working_dir, symlink_path))
        except OSError:
            # Skip if symlinks not supported on this system
            self.skipTest("Symlinks not supported on this system")
    
    def test_traversal_attack_prevention(self):
        """Test prevention of directory traversal attacks"""
        old_cwd = os.getcwd()
        try:
            os.chdir(self.working_dir)
            # These should all be denied as they don't exist or go outside working dir
            self.assertFalse(is_directory_allowed(".", "../sibling"))
            self.assertFalse(is_directory_allowed(".", "../../"))
            self.assertFalse(is_directory_allowed(".", "../../../etc"))
        finally:
            os.chdir(old_cwd)


if __name__ == '__main__':
    unittest.main()
