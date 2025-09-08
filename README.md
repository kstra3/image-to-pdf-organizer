# 🚀 Image-to-PDF Organizer Professional v2.0

A powerful, professional-grade application for converting and organizing images into PDF documents with advanced features, multiple interfaces, and extensibility.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Production-green)

## ✨ Key Features

### 🎯 **Multiple Interfaces**
- **Advanced GUI** (PyQt5): Professional dark-themed interface with drag-drop
- **Basic GUI** (Tkinter): Simple, lightweight interface for basic operations  
- **Enhanced CLI**: Feature-rich command-line with progress indicators and colors
- **Smart Launcher**: Automatically detects and launches the best available interface

### 🔧 **Advanced Image Processing**
- **Auto-Enhancement**: Intelligent brightness, contrast, and color adjustment
- **Auto-Rotation**: Automatic orientation correction based on EXIF data
- **Watermarking**: Text and image watermarking capabilities
- **Effects & Filters**: Blur, sharpen, sepia, vintage, and artistic effects
- **Batch Processing**: Process multiple images with consistent settings

### 📄 **Professional PDF Creation**
- **Multiple Page Sizes**: A4, Letter, Legal, Tabloid, and custom fit options
- **Smart Compression**: Optimal quality-to-size ratio with customizable settings
- **Layout Options**: Center images, maintain aspect ratios, custom margins
- **Quality Control**: Fine-grained compression control (1-100%)

### 🗂️ **Project Management**
- **Save/Load Projects**: Preserve image arrangements and settings
- **Project Templates**: Pre-configured setups for common use cases
- **Recent Projects**: Quick access to recently used projects
- **Import/Export**: Share project configurations

### 🔌 **Plugin System**
- **Extensible Architecture**: Add custom image processing and PDF features
- **Plugin Manager**: Easy installation and management of extensions
- **Example Plugins**: Image effects, advanced filters, and more
- **Developer API**: Create your own plugins with comprehensive documentation

### ⚙️ **Configuration & Management**
- **Smart Settings**: Persistent configuration with user preferences
- **Performance Tuning**: Memory limits, concurrent operations, caching
- **Logging System**: Comprehensive logging for troubleshooting
- **Auto-Updates**: Built-in update checking (configurable)

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pdf_image
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Launch Options

```bash
# Auto-detect best interface
python main.py

# Force specific interface
python main.py --gui pyqt5      # Advanced GUI
python main.py --gui tkinter    # Basic GUI
python main.py --cli           # Enhanced CLI

# Show launcher menu
python main.py --launcher

# Windows batch launcher
smart_launcher.bat
```

## 📖 Usage Examples

### GUI Interface
- **Drag & Drop**: Simply drag images into the application window
- **Reorder**: Drag images to rearrange the order in your PDF
- **Settings**: Configure page size, compression, and enhancement options
- **Preview**: See image thumbnails and PDF layout before conversion
- **Export**: Choose output location and create your PDF

### Command Line Interface

#### Basic Conversion
```bash
python -m src.cli_enhanced photo1.jpg photo2.png -o album.pdf
```

#### Advanced Usage
```bash
# Batch processing with enhancement
python -m src.cli_enhanced vacation/*.jpg -o vacation.pdf \
  --page-size LETTER --compress --quality 80 --enhance --auto-rotate

# Add watermark
python -m src.cli_enhanced documents/*.png -o watermarked.pdf \
  --watermark "CONFIDENTIAL" --quality 90

# Quiet mode for scripting
python -m src.cli_enhanced batch/*.jpg -o output.pdf --quiet
```

#### CLI Options
- `-o, --output`: Output PDF file path
- `-s, --page-size`: PDF page size (A4, LETTER, LEGAL, TABLOID, FIT)
- `-c, --compress`: Enable image compression
- `-q, --quality`: Compression quality (1-100)
- `--enhance`: Apply automatic image enhancement
- `--auto-rotate`: Auto-rotate based on EXIF orientation
- `--watermark TEXT`: Add text watermark
- `--quiet`: Minimal output for scripting
- `--verbose`: Detailed progress information

## 🏗️ Architecture

### Project Structure
```
pdf_image/
├── src/
│   ├── services/           # Core business logic
│   │   ├── image_handler.py
│   │   ├── pdf_converter.py
│   │   ├── advanced_processor.py
│   │   └── project_manager.py
│   ├── gui/               # User interfaces
│   │   ├── app.py         # Tkinter GUI
│   │   └── gui_2.py       # PyQt5 GUI
│   ├── launcher.py        # Smart GUI launcher
│   ├── cli_enhanced.py    # Enhanced command line
│   ├── settings_manager.py # Configuration management
│   ├── plugin_system.py   # Plugin architecture
│   └── help_system.py     # Interactive help
├── plugins/               # Plugin directory
│   └── image_effects/     # Example plugin
├── tests/                 # Test suite
├── requirements.txt       # Dependencies
├── main.py               # Main entry point
└── smart_launcher.bat    # Windows launcher
```

### Core Components

- **ImageHandler**: Image validation, processing, and optimization
- **PDFConverter**: PDF creation with advanced layout options
- **AdvancedImageProcessor**: Enhanced image processing capabilities
- **ProjectManager**: Project persistence and management
- **PluginSystem**: Extensible plugin architecture
- **SettingsManager**: Configuration and preferences
- **HelpSystem**: Interactive documentation and assistance

## 🔌 Plugin Development

### Creating a Plugin

1. **Create plugin directory**:
   ```
   plugins/my_plugin/
   ├── manifest.json
   └── main.py
   ```

2. **Define manifest.json**:
   ```json
   {
     "name": "My Plugin",
     "version": "1.0.0",
     "description": "Plugin description",
     "author": "Your Name",
     "main_module": "main",
     "plugin_class": "MyPlugin"
   }
   ```

3. **Implement plugin class**:
   ```python
   from src.plugin_system import ImageProcessorPlugin
   
   class MyPlugin(ImageProcessorPlugin):
       @property
       def name(self) -> str:
           return "My Plugin"
       
       def process_image(self, image_path: str, **kwargs) -> str:
           # Your processing logic
           return processed_image_path
   ```

### Plugin Types
- **ImageProcessorPlugin**: Custom image effects and processing
- **PDFProcessorPlugin**: PDF manipulation and enhancement
- **UIPlugin**: Interface extensions and custom tools

## 🔧 Configuration

### Settings Management
```bash
# View current settings
python main.py --settings

# Reset to defaults
python main.py --reset-settings

# Show plugin information
python main.py --plugins
```

### Performance Tuning
Edit settings or use the settings GUI to configure:
- **Memory limits**: Prevent out-of-memory errors
- **Concurrent operations**: Balance speed vs. system load
- **Compression settings**: Default quality and methods
- **Temporary directories**: Manage disk space usage

## 🆘 Help & Support

### Built-in Help System
```bash
# Open comprehensive documentation
python main.py --show-help

# List help topics
python main.py --help-topics

# Quick help for specific topics
python main.py --quick-help "image processing"
```

### Troubleshooting

#### Common Issues
1. **PyQt5 Platform Plugin Error**:
   - Reinstall PyQt5: `pip uninstall PyQt5 && pip install PyQt5`
   - Use fallback: `python main.py --gui tkinter`

2. **Memory Issues with Large Images**:
   - Enable compression: Use `--compress` flag
   - Reduce image size: Configure max dimensions in settings
   - Process in smaller batches

3. **Permission Errors**:
   - Run with appropriate permissions
   - Choose accessible output directory
   - Check disk space availability

### Getting Help
- Use the built-in help system: `python main.py --show-help`
- Check the troubleshooting guide in the help documentation
- Enable debug logging: `python main.py --log-level DEBUG`

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test module
pytest tests/test_image_handler.py
```

## 📦 Distribution

### Creating Standalone Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py
```

### Package Structure for Distribution
```
dist/
├── ImageToPDF-Organizer/
│   ├── main.exe           # Windows executable
│   ├── plugins/           # Plugin directory
│   ├── documentation/     # Help files
│   └── examples/          # Sample files
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all public methods
- Include tests for new features
- Update documentation as needed
- Ensure backward compatibility

## 📝 Changelog

### Version 2.0.0 (Latest)
- ✅ **Major Architecture Overhaul**: Modular, extensible design
- ✅ **Advanced PyQt5 GUI**: Professional interface with dark theme
- ✅ **Enhanced CLI**: Progress bars, colors, advanced options
- ✅ **Plugin System**: Extensible architecture for custom features
- ✅ **Project Management**: Save/load image arrangements
- ✅ **Advanced Image Processing**: Enhancement, effects, watermarking
- ✅ **Smart Configuration**: Persistent settings with user preferences
- ✅ **Comprehensive Help**: Interactive documentation system
- ✅ **Performance Optimization**: Memory management, batch processing
- ✅ **Error Handling**: Robust error recovery and user feedback

### Previous Versions
- **v1.1**: Added PyQt5 GUI, improved error handling
- **v1.0**: Initial release with basic Tkinter GUI and CLI

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pillow**: Python Imaging Library for image processing
- **img2pdf**: Efficient image-to-PDF conversion
- **PyQt5**: Professional GUI framework
- **Contributors**: Thanks to all contributors and beta testers

---

**Image-to-PDF Organizer Professional v2.0**  
*Transform your images into professional PDF documents with ease and style.*
