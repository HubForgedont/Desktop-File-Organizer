#!/usr/bin/env python3
"""
Tests for Desktop File Organizer
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from organizer import DesktopOrganizer


class TestDesktopOrganizer(unittest.TestCase):
    """Test cases for the DesktopOrganizer class."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory to simulate desktop
        self.test_dir = tempfile.mkdtemp()
        
        # Create test config
        self.config = {
            'categories': {
                'Documents': ['.txt', '.pdf'],
                'Images': ['.jpg', '.png']
            },
            'excluded_files': ['.DS_Store'],
            'excluded_folders': ['Organized_Files'],
            'target_directory': 'Organized_Files'
        }
        
        # Create a test config file
        self.config_path = os.path.join(self.test_dir, 'test_config.yaml')
        with open(self.config_path, 'w') as f:
            import yaml
            yaml.dump(self.config, f)
        
        # Create test files
        self.create_test_files()
        
        # Initialize organizer with test config
        self.organizer = DesktopOrganizer(self.config_path)
        # Override desktop path for testing
        self.organizer.desktop_path = self.test_dir

    def create_test_files(self):
        """Create test files in the test directory."""
        # Create some test files
        open(os.path.join(self.test_dir, 'document1.txt'), 'w').close()
        open(os.path.join(self.test_dir, 'document2.pdf'), 'w').close()
        open(os.path.join(self.test_dir, 'image1.jpg'), 'w').close()
        open(os.path.join(self.test_dir, 'image2.png'), 'w').close()
        open(os.path.join(self.test_dir, 'unknown.xyz'), 'w').close()
        open(os.path.join(self.test_dir, '.DS_Store'), 'w').close()
        
        # Create an excluded folder
        os.makedirs(os.path.join(self.test_dir, 'Organized_Files'), exist_ok=True)

    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.test_dir)

    def test_organize_files(self):
        """Test that files are organized correctly."""
        # Run the organizer
        moved_count = self.organizer.organize_files()
        
        # Check that the correct number of files were moved
        self.assertEqual(moved_count, 5)
        
        # Check that files are in the correct categories
        target_dir = os.path.join(self.test_dir, 'Organized_Files')
        
        # Check Documents folder
        docs_dir = os.path.join(target_dir, 'Documents')
        self.assertTrue(os.path.exists(docs_dir))
        self.assertTrue(os.path.exists(os.path.join(docs_dir, 'document1.txt')))
        self.assertTrue(os.path.exists(os.path.join(docs_dir, 'document2.pdf')))
        
        # Check Images folder
        images_dir = os.path.join(target_dir, 'Images')
        self.assertTrue(os.path.exists(images_dir))
        self.assertTrue(os.path.exists(os.path.join(images_dir, 'image1.jpg')))
        self.assertTrue(os.path.exists(os.path.join(images_dir, 'image2.png')))
        
        # Check Other folder
        other_dir = os.path.join(target_dir, 'Other')
        self.assertTrue(os.path.exists(other_dir))
        self.assertTrue(os.path.exists(os.path.join(other_dir, 'unknown.xyz')))
        
        # Check that excluded files were not moved
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, '.DS_Store')))

    def test_undo_organization(self):
        """Test that undo functionality works correctly."""
        # First organize files
        self.organizer.organize_files()
        
        # Then undo the organization
        restored_count = self.organizer.undo_last_organization()
        
        # Check that the correct number of files were restored
        self.assertEqual(restored_count, 5)
        
        # Check that files are back in their original location
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'document1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'document2.pdf')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'image1.jpg')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'image2.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'unknown.xyz')))


if __name__ == '__main__':
    unittest.main()
