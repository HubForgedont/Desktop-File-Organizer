```markdown
# Desktop File Organizer

A simple yet powerful Python tool to automatically organize files on your desktop into categorized folders.

## Features

- **Automatic Categorization**: Files are automatically sorted based on their extensions
- **Customizable Categories**: Define your own file categories and extensions
- **Undo Functionality**: Easily revert the last organization operation
- **Scheduling**: Set up automatic organization at regular intervals
- **Detailed Logging**: Keep track of all file movements
- **Exclusion Rules**: Specify files and folders to exclude from organization

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/HubForgedont/desktop-file-organizer.git
   ```

2. Navigate to the project directory:
   ```
   cd desktop-file-organizer
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

To organize your desktop files:

```
python organizer.py
```

This will create a folder called "Organized_Files" on your desktop and sort all files into appropriate subfolders.

### Command Line Options

- `--config PATH`: Specify a custom configuration file path
- `--undo`: Undo the last organization operation
- `--schedule MINUTES`: Schedule automatic organization every N minutes

Examples:

```
# Use a custom configuration file
python organizer.py --config my_config.yaml

# Undo the last organization
python organizer.py --undo

# Schedule organization every 30 minutes
python organizer.py --schedule 30
```

## Configuration

The default configuration file (`config.yaml`) categorizes files as follows:

| Category | File Extensions |
|----------|----------------|
| Documents | .pdf, .docx, .txt, .doc, .rtf, .odt, .xlsx, .pptx, .csv |
| Images | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .tiff |
| Videos | .mp4, .mov, .avi, .mkv, .wmv, .flv, .webm |
| Audio | .mp3, .wav, .ogg, .flac, .aac, .m4a |
| Archives | .zip, .rar, .7z, .tar, .gz, .bz2 |
| Code | .py, .js, .html, .css, .java, .cpp, .c, .go, .php, .rb, .json, .xml |
| Executables | .exe, .msi, .app, .dmg, .sh |

You can customize the categories and file extensions by editing the `config.yaml` file.

## Screenshots

### Before Organization
![Before Organization](https://raw.githubusercontent.com/HubForgedont/desktop-file-organizer/main/screenshots/before.png)

### After Organization
![After Organization](https://raw.githubusercontent.com/HubForgedont/desktop-file-organizer/main/screenshots/after.png)

## Running Tests

To run the test suite:

```
python -m unittest tests/test_organizer.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need to keep desktops clean and organized
- Thanks to all contributors who have helped improve this tool
```
