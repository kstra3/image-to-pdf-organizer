# Quick Start Guide

## Image-to-PDF Organizer Pro

### Installation (Windows)

1. **Easy Installation**: Double-click `install_windows.bat` to automatically set up everything.

2. **Manual Installation**:
   ```
   pip install pillow img2pdf PyQt5
   ```

### Running the Application

1. **Advanced GUI (PyQt5)** ⭐ **Recommended**: 
   - Double-click `run_advanced_gui.bat` or run:
   ```
   python -m src.main --qt
   ```

2. **Basic GUI (Tkinter)**: Double-click `run_app.bat` or run:
   ```
   python -m src.main --gui tkinter
   ```

3. **Command Line**: 
   ```
   python -m src.main image1.jpg image2.png -o output.pdf
   ```

### Using the Advanced GUI

1. **Add Images**: 
   - Drag and drop images directly into the application
   - Or click "Add Images" to select files
   - Supports JPG, PNG, BMP, TIFF, GIF formats

2. **Organize**: 
   - View thumbnails of all images
   - Use ▲▼ buttons to reorder (or drag to reorder - coming soon)
   - Click on any image to see a full preview

3. **Configure Options**: 
   - **PDF Options Tab**: Set page size (A4, Letter, etc.) and compression
   - **Advanced Tab**: Future features like watermarking
   - **Batch Tab**: Configure batch processing settings
   - **Preview Tab**: View selected image details and metadata

4. **Export**: Click "Export as PDF" and choose where to save

### Advanced GUI Features

- **Dark Theme**: Easy on the eyes professional interface
- **Live Thumbnails**: See all your images at a glance
- **Drag & Drop**: Native support for dragging files
- **Real-time Preview**: Click any image for full-size preview
- **Progress Tracking**: Visual progress bar during conversion
- **Keyboard Shortcuts**: 
  - `Ctrl+N` - New Project
  - `Ctrl+O` - Add Images  
  - `Ctrl+E` - Export PDF
  - `Ctrl+Q` - Exit
- **Status Updates**: Real-time feedback in the status bar
- **Resizable Interface**: Adjust panels to fit your workflow

### Command Line Options

- `-o, --output`: Output PDF file path (default: output.pdf)
- `-s, --page-size`: Page size (A4, LETTER, LEGAL, TABLOID, FIT)
- `-c, --compress`: Enable compression
- `-q, --quality`: Compression quality (1-100)

### Examples

```bash
# Basic conversion
python -m src.main *.jpg -o family_photos.pdf

# With compression and custom size
python -m src.main vacation/*.png -o vacation.pdf -s LETTER -c -q 80

# Fit to original image size
python -m src.main screenshot.png -o screenshot.pdf -s FIT
```

### Troubleshooting

- **Import errors**: Run `pip install -r requirements.txt`
- **GUI won't start**: Check if tkinter is installed with your Python
- **Permission errors**: Make sure you have write access to the output directory
