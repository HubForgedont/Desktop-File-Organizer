#!/usr/bin/env python3
"""
Desktop File Organizer
A tool to automatically organize files on your desktop into appropriate folders.
"""

import os
import shutil
import logging
import yaml
import time
import argparse
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/file_movements.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('DesktopOrganizer')

class DesktopOrganizer:
    """Main class for organizing desktop files."""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize the organizer with configuration."""
        self.load_config(config_path)
        self.desktop_path = self.get_desktop_path()
        self.moved_files = []  # Track moved files for undo operation
        
        # Create log directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
    
    def load_config(self, config_path):
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {config_path}")
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}. Creating default config.")
            self.config = self.create_default_config()
            self.save_config(config_path)
    
    def create_default_config(self):
        """Create default configuration."""
        return {
            'categories': {
                'Documents': ['.pdf', '.docx', '.txt', '.doc', '.rtf', '.odt'],
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv'],
                'Audio': ['.mp3', '.wav', '.ogg', '.flac', '.aac'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.go', '.php']
            },
            'excluded_files': ['.DS_Store', 'desktop.ini'],
            'excluded_folders': ['Organized_Files'],
            'target_directory': 'Organized_Files'
        }
    
    def save_config(self, config_path):
        """Save configuration to YAML file."""
        with open(config_path, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)
        logger.info(f"Configuration saved to {config_path}")
    
    def get_desktop_path(self):
        """Get the path to the user's desktop."""
        return str(Path.home() / "Desktop")
    
    def organize_files(self):
        """Organize files on the desktop into categorized folders."""
        logger.info("Starting desktop organization")
        
        # Create target directory if it doesn't exist
        target_dir = os.path.join(self.desktop_path, self.config['target_directory'])
        os.makedirs(target_dir, exist_ok=True)
        
        # Clear moved files list for new organization
        self.moved_files = []
        
        # Process each file on desktop
        for item in os.listdir(self.desktop_path):
            item_path = os.path.join(self.desktop_path, item)
            
            # Skip if it's a directory or excluded
            if (os.path.isdir(item_path) or 
                item in self.config['excluded_files'] or
                item in self.config['excluded_folders']):
                continue
            
            # Determine category based on file extension
            file_ext = os.path.splitext(item)[1].lower()
            category = "Other"  # Default category
            
            for cat, extensions in self.config['categories'].items():
                if file_ext in extensions:
                    category = cat
                    break
            
            # Create category folder if it doesn't exist
            category_path = os.path.join(target_dir, category)
            os.makedirs(category_path, exist_ok=True)
            
            # Move the file
            destination = os.path.join(category_path, item)
            try:
                shutil.move(item_path, destination)
                self.moved_files.append((item_path, destination))
                logger.info(f"Moved {item} to {category}")
            except Exception as e:
                logger.error(f"Error moving {item}: {e}")
        
        logger.info("Desktop organization completed")
        return len(self.moved_files)
    
    def undo_last_organization(self):
        """Undo the last organization operation."""
        if not self.moved_files:
            logger.info("No files to restore")
            return 0
        
        restored_count = 0
        for original_path, current_path in reversed(self.moved_files):
            try:
                if os.path.exists(current_path):
                    shutil.move(current_path, original_path)
                    logger.info(f"Restored {os.path.basename(current_path)} to original location")
                    restored_count += 1
            except Exception as e:
                logger.error(f"Error restoring {os.path.basename(current_path)}: {e}")
        
        self.moved_files = []
        logger.info(f"Restored {restored_count} files to their original locations")
        return restored_count
    
    def schedule_organization(self, interval_minutes=60):
        """Schedule automatic organization at specified intervals."""
        logger.info(f"Scheduled organization every {interval_minutes} minutes. Press Ctrl+C to stop.")
        try:
            while True:
                self.organize_files()
                logger.info(f"Waiting {interval_minutes} minutes until next organization...")
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            logger.info("Scheduled organization stopped by user")


def main():
    """Main function to parse arguments and run the organizer."""
    parser = argparse.ArgumentParser(description='Organize desktop files into folders.')
    parser.add_argument('--config', default='config.yaml', help='Path to configuration file')
    parser.add_argument('--undo', action='store_true', help='Undo the last organization')
    parser.add_argument('--schedule', type=int, help='Schedule organization every N minutes')
    
    args = parser.parse_args()
    
    organizer = DesktopOrganizer(args.config)
    
    if args.undo:
        count = organizer.undo_last_organization()
        print(f"Restored {count} files to their original locations")
    elif args.schedule:
        organizer.schedule_organization(args.schedule)
    else:
        count = organizer.organize_files()
        print(f"Organized {count} files on your desktop")


if __name__ == "__main__":
    main()
