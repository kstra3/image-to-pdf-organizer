"""
Interactive help system and documentation generator.
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import webbrowser
import tempfile


class HelpSystem:
    """Interactive help system for the application."""
    
    def __init__(self):
        """Initialize the help system."""
        self.help_data = self._load_help_data()
        self.topics = self._build_topic_index()
    
    def _load_help_data(self) -> Dict[str, Any]:
        """Load help data."""
        return {
            'getting_started': {
                'title': 'Getting Started',
                'content': '''
# Getting Started with Image-to-PDF Organizer

Welcome to the Image-to-PDF Organizer! This powerful tool helps you convert images to PDF with advanced features.

## Quick Start
1. Launch the application using `python main.py` or the GUI launcher
2. Add images by clicking "Add Images" or dragging and dropping
3. Arrange images in your desired order
4. Configure PDF settings (page size, compression, etc.)
5. Click "Convert to PDF" to create your document

## Interface Options
- **Basic GUI**: Simple Tkinter interface for basic operations
- **Advanced GUI**: Feature-rich PyQt5 interface with dark theme
- **Command Line**: Powerful CLI with batch processing capabilities

## Key Features
- Drag-and-drop image management
- Advanced image processing (enhancement, watermarking, rotation)
- Multiple PDF page sizes and compression options
- Project management (save/load arrangements)
- Batch processing capabilities
- Plugin system for extensibility
                ''',
                'keywords': ['start', 'begin', 'introduction', 'quick', 'launch']
            },
            
            'image_processing': {
                'title': 'Image Processing',
                'content': '''
# Image Processing Features

## Supported Formats
- JPEG/JPG: Most common format, supports compression
- PNG: Supports transparency
- BMP: Windows bitmap format
- TIFF: High-quality format
- GIF: Animated images (first frame used)

## Image Enhancement
- **Auto Enhance**: Automatically adjusts brightness, contrast, and color
- **Auto Rotate**: Rotates images based on EXIF orientation data
- **Resize**: Scale images to fit PDF pages optimally
- **Compression**: Reduce file size while maintaining quality

## Advanced Processing
- **Watermarking**: Add text or image watermarks
- **Effects**: Apply filters like blur, sharpen, sepia, vintage
- **Batch Processing**: Process multiple images with same settings
- **Quality Control**: Adjust compression quality (1-100%)

## Using the Advanced Processor
```python
from src.services.advanced_processor import AdvancedImageProcessor

processor = AdvancedImageProcessor()
enhanced = processor.enhance_image("input.jpg")
rotated = processor.auto_rotate_image(enhanced)
watermarked = processor.add_text_watermark(rotated, "Confidential")
```
                ''',
                'keywords': ['image', 'process', 'enhance', 'rotate', 'watermark', 'compress']
            },
            
            'pdf_conversion': {
                'title': 'PDF Conversion',
                'content': '''
# PDF Conversion Options

## Page Sizes
- **A4**: Standard international format (210×297mm)
- **Letter**: US standard format (8.5×11 inches)
- **Legal**: US legal format (8.5×14 inches)
- **Tabloid**: Large format (11×17 inches)
- **Fit**: Preserve original image dimensions

## Compression Settings
- **Quality**: 1-100 (higher = better quality, larger file)
- **Auto Compression**: Intelligently balance quality and size
- **Lossless**: Preserve original quality (larger files)

## Advanced Options
- **Fit to Page**: Scale images to fit page boundaries
- **Maintain Aspect Ratio**: Prevent image distortion
- **Center Images**: Center images on pages
- **Add Margins**: Add white space around images

## Using the Converter
```python
from src.services.pdf_converter import PDFConverter

converter = PDFConverter()
pdf_path = converter.convert_images_to_pdf(
    image_paths=["img1.jpg", "img2.png"],
    output_path="output.pdf",
    page_size="A4",
    compress=True,
    compression_quality=85
)
```
                ''',
                'keywords': ['pdf', 'convert', 'page', 'size', 'compress', 'quality']
            },
            
            'cli_usage': {
                'title': 'Command Line Usage',
                'content': '''
# Command Line Interface

## Basic Usage
```bash
python -m src.cli_enhanced image1.jpg image2.png -o output.pdf
```

## Advanced Options
```bash
# With compression and custom page size
python -m src.cli_enhanced *.jpg -o album.pdf -s LETTER -c -q 80

# Apply enhancements
python -m src.cli_enhanced photos/*.png -o enhanced.pdf --enhance --auto-rotate

# Add watermark
python -m src.cli_enhanced docs/*.jpg -o watermarked.pdf --watermark "DRAFT"

# Quiet mode for scripting
python -m src.cli_enhanced input/*.png -o batch.pdf --quiet
```

## Options Reference
- `-o, --output`: Output PDF file path
- `-s, --page-size`: PDF page size (A4, LETTER, LEGAL, TABLOID, FIT)
- `-c, --compress`: Enable compression
- `-q, --quality`: Compression quality (1-100)
- `--enhance`: Apply automatic enhancement
- `--auto-rotate`: Auto-rotate based on EXIF data
- `--watermark TEXT`: Add text watermark
- `--quiet`: Minimal output
- `--verbose`: Detailed output

## Batch Processing
The CLI supports wildcards and batch processing:
```bash
# Process all images in directory
python -m src.cli_enhanced photos/* -o album.pdf

# Process specific types
python -m src.cli_enhanced **/*.{jpg,png} -o combined.pdf
```
                ''',
                'keywords': ['cli', 'command', 'line', 'batch', 'script', 'terminal']
            },
            
            'project_management': {
                'title': 'Project Management',
                'content': '''
# Project Management

## Overview
Projects allow you to save and restore image arrangements, settings, and metadata for later use.

## Project Structure
```json
{
  "name": "My Project",
  "created": "2024-01-01T12:00:00",
  "images": [
    {
      "path": "/path/to/image1.jpg",
      "order": 0,
      "settings": {...}
    }
  ],
  "pdf_settings": {
    "page_size": "A4",
    "compression": true,
    "quality": 85
  }
}
```

## Using Project Manager
```python
from src.services.project_manager import ProjectManager

manager = ProjectManager()

# Create project
project_data = {
    "name": "Vacation Photos",
    "images": image_list,
    "pdf_settings": pdf_config
}
project_path = manager.save_project(project_data, "vacation.json")

# Load project
loaded_project = manager.load_project(project_path)

# List recent projects
recent = manager.get_recent_projects()
```

## Best Practices
1. Use descriptive project names
2. Organize projects by topic or date
3. Include relevant metadata
4. Regular cleanup of old projects
5. Backup important projects

## GUI Integration
The advanced GUI provides:
- Project browser
- Quick save/load
- Recent projects menu
- Project templates
- Import/export functionality
                ''',
                'keywords': ['project', 'save', 'load', 'manage', 'template']
            },
            
            'plugins': {
                'title': 'Plugin System',
                'content': '''
# Plugin System

## Overview
The plugin system allows you to extend the application with custom functionality.

## Plugin Types
1. **Image Processor Plugins**: Custom image effects and filters
2. **PDF Processor Plugins**: PDF manipulation and enhancement
3. **UI Plugins**: Interface extensions and tools

## Creating a Plugin

### 1. Create Plugin Directory
```
plugins/
  my_plugin/
    manifest.json
    main.py
```

### 2. Define Manifest
```json
{
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": "Your Name",
  "main_module": "main",
  "plugin_class": "MyPlugin",
  "dependencies": ["required_package"],
  "min_app_version": "2.0.0",
  "enabled": true
}
```

### 3. Implement Plugin Class
```python
from plugin_system import ImageProcessorPlugin

class MyPlugin(ImageProcessorPlugin):
    @property
    def name(self) -> str:
        return "My Plugin"
    
    def initialize(self) -> bool:
        return True
    
    def process_image(self, image_path: str, **kwargs) -> str:
        # Your processing logic here
        return processed_image_path
```

## Managing Plugins
```python
from src.plugin_system import get_plugin_manager

manager = get_plugin_manager()

# Load all plugins
manager.load_all_plugins()

# Get specific plugin
plugin = manager.get_plugin("Image Effects")

# List available plugins
for plugin_info in manager.get_plugin_info():
    print(f"{plugin_info['name']}: {'Loaded' if plugin_info['loaded'] else 'Available'}")
```

## Example Plugins
- **Image Effects**: Blur, sharpen, sepia, vintage effects
- **Watermark Tools**: Advanced watermarking options
- **Format Converters**: Additional format support
                ''',
                'keywords': ['plugin', 'extend', 'custom', 'effect', 'filter']
            },
            
            'troubleshooting': {
                'title': 'Troubleshooting',
                'content': '''
# Troubleshooting Guide

## Common Issues

### PyQt5 Platform Plugin Error
**Problem**: "Qt platform plugin 'windows' could not be found"
**Solutions**:
1. Reinstall PyQt5: `pip uninstall PyQt5 && pip install PyQt5`
2. Use fallback GUI: Launch with `--gui tkinter`
3. Check Qt installation: Run diagnostic script

### Memory Issues with Large Images
**Problem**: Application crashes or slows down with large images
**Solutions**:
1. Enable compression: Use `-c` flag or enable in GUI
2. Reduce image size: Set max dimensions in settings
3. Process in batches: Split large operations
4. Increase memory limit in settings

### Import Errors
**Problem**: "Module not found" errors
**Solutions**:
1. Check virtual environment activation
2. Install missing dependencies: `pip install -r requirements.txt`
3. Verify Python path configuration
4. Reinstall problematic packages

### Permission Errors
**Problem**: Cannot save files or access directories
**Solutions**:
1. Run with administrator privileges (Windows)
2. Check file/directory permissions
3. Choose different output location
4. Ensure disk space availability

## Performance Optimization

### Image Processing
- Use appropriate compression settings
- Enable auto-enhancement only when needed
- Process similar images in batches
- Clean up temporary files regularly

### Memory Management
- Close unused applications
- Monitor system resources
- Use 64-bit Python for large datasets
- Configure appropriate memory limits

## Debug Mode
Enable verbose logging for troubleshooting:
```bash
python main.py --verbose --log-level DEBUG
```

## Getting Help
1. Check this help system
2. Review error messages carefully
3. Enable debug logging
4. Check plugin compatibility
5. Verify system requirements

## Reporting Issues
When reporting problems, include:
- Operating system and version
- Python version
- Error messages (full text)
- Steps to reproduce
- Sample files (if relevant)
                ''',
                'keywords': ['error', 'problem', 'fix', 'debug', 'crash', 'slow']
            }
        }
    
    def _build_topic_index(self) -> Dict[str, str]:
        """Build search index for topics."""
        index = {}
        for topic_id, topic_data in self.help_data.items():
            # Index by topic ID
            index[topic_id] = topic_id
            
            # Index by title
            title = topic_data['title'].lower()
            index[title] = topic_id
            
            # Index by keywords
            for keyword in topic_data.get('keywords', []):
                index[keyword.lower()] = topic_id
        
        return index
    
    def search_help(self, query: str) -> List[Dict[str, str]]:
        """
        Search for help topics.
        
        Args:
            query: Search query
            
        Returns:
            List of matching topics
        """
        query = query.lower().strip()
        matches = []
        
        for topic_id, topic_data in self.help_data.items():
            # Check title
            if query in topic_data['title'].lower():
                matches.append({
                    'id': topic_id,
                    'title': topic_data['title'],
                    'relevance': 'high'
                })
                continue
            
            # Check keywords
            for keyword in topic_data.get('keywords', []):
                if query in keyword.lower():
                    matches.append({
                        'id': topic_id,
                        'title': topic_data['title'],
                        'relevance': 'medium'
                    })
                    break
            
            # Check content
            if query in topic_data['content'].lower():
                matches.append({
                    'id': topic_id,
                    'title': topic_data['title'],
                    'relevance': 'low'
                })
        
        # Sort by relevance
        relevance_order = {'high': 0, 'medium': 1, 'low': 2}
        matches.sort(key=lambda x: relevance_order.get(x['relevance'], 3))
        
        return matches
    
    def get_topic(self, topic_id: str) -> Optional[Dict[str, str]]:
        """
        Get help topic by ID.
        
        Args:
            topic_id: Topic identifier
            
        Returns:
            Topic data or None if not found
        """
        return self.help_data.get(topic_id)
    
    def list_topics(self) -> List[Dict[str, str]]:
        """
        List all available help topics.
        
        Returns:
            List of topics with ID and title
        """
        return [
            {'id': topic_id, 'title': topic_data['title']}
            for topic_id, topic_data in self.help_data.items()
        ]
    
    def generate_html_help(self, output_dir: str) -> str:
        """
        Generate HTML help documentation.
        
        Args:
            output_dir: Directory to save HTML files
            
        Returns:
            Path to main help file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate CSS
        css_content = '''
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        h3 { color: #7f8c8d; }
        code {
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }
        .nav {
            background: #34495e;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .nav a {
            color: white;
            text-decoration: none;
            margin-right: 20px;
            padding: 5px 10px;
            border-radius: 3px;
        }
        .nav a:hover {
            background: #4a5d7a;
        }
        .search-box {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        '''
        
        css_file = output_path / 'style.css'
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Generate navigation
        nav_links = []
        for topic_id, topic_data in self.help_data.items():
            nav_links.append(f'<a href="{topic_id}.html">{topic_data["title"]}</a>')
        
        nav_html = f'<div class="nav">{" ".join(nav_links)}</div>'
        
        # Generate topic pages
        for topic_id, topic_data in self.help_data.items():
            content = topic_data['content'].replace('\n', '<br>\n')
            
            # Simple markdown-like processing
            import re
            content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
            content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
            content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
            content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
            content = re.sub(r'```([^`]+)```', r'<pre>\1</pre>', content, flags=re.DOTALL)
            
            html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>{topic_data["title"]} - Image-to-PDF Organizer Help</title>
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
                <div class="container">
                    {nav_html}
                    {content}
                </div>
            </body>
            </html>
            '''
            
            topic_file = output_path / f'{topic_id}.html'
            with open(topic_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        # Generate index page
        topic_list = []
        for topic_id, topic_data in self.help_data.items():
            topic_list.append(f'<li><a href="{topic_id}.html">{topic_data["title"]}</a></li>')
        
        index_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Image-to-PDF Organizer - Help Documentation</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <div class="container">
                <h1>Image-to-PDF Organizer Help</h1>
                <input type="text" class="search-box" placeholder="Search help topics..." 
                       onkeyup="searchTopics(this.value)">
                
                <h2>Available Topics</h2>
                <ul id="topic-list">
                    {"".join(topic_list)}
                </ul>
                
                <script>
                function searchTopics(query) {{
                    const topics = document.querySelectorAll('#topic-list li');
                    query = query.toLowerCase();
                    
                    topics.forEach(topic => {{
                        const text = topic.textContent.toLowerCase();
                        topic.style.display = text.includes(query) ? 'block' : 'none';
                    }});
                }}
                </script>
            </div>
        </body>
        </html>
        '''
        
        index_file = output_path / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        return str(index_file)
    
    def show_help_in_browser(self, topic_id: str = None):
        """
        Generate and show help in web browser.
        
        Args:
            topic_id: Specific topic to show, or None for index
        """
        temp_dir = tempfile.mkdtemp(prefix='pdf_organizer_help_')
        help_file = self.generate_html_help(temp_dir)
        
        if topic_id and topic_id in self.help_data:
            help_file = os.path.join(temp_dir, f'{topic_id}.html')
        
        webbrowser.open(f'file://{help_file}')
    
    def get_quick_help(self, topic: str) -> str:
        """
        Get quick help text for a topic.
        
        Args:
            topic: Topic name or keyword
            
        Returns:
            Quick help text
        """
        matches = self.search_help(topic)
        if matches:
            topic_data = self.get_topic(matches[0]['id'])
            if topic_data:
                # Extract first paragraph as quick help
                content = topic_data['content']
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        return line
        
        return f"No help available for '{topic}'. Try 'help topics' to see available topics."


# Global help system instance
_help_system = None


def get_help_system() -> HelpSystem:
    """Get the global help system instance."""
    global _help_system
    if _help_system is None:
        _help_system = HelpSystem()
    return _help_system


def show_help(topic: str = None):
    """Show help for a topic."""
    help_system = get_help_system()
    if topic:
        help_system.show_help_in_browser(topic)
    else:
        help_system.show_help_in_browser()


def search_help(query: str) -> List[Dict[str, str]]:
    """Search help topics."""
    help_system = get_help_system()
    return help_system.search_help(query)


def quick_help(topic: str) -> str:
    """Get quick help for a topic."""
    help_system = get_help_system()
    return help_system.get_quick_help(topic)
