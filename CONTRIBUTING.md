# Contributing to Image-to-PDF Organizer

We welcome contributions to make this project even better! 🎉

## 🚀 Quick Start for Contributors

### 1. Fork & Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/image-to-pdf-organizer.git
cd image-to-pdf-organizer
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 3. Test Your Setup
```bash
# Run tests
pytest

# Launch GUI to test
python main.py --gui pyqt5
```

## 🛠️ Development Areas

### Easy Contributions (Good First Issues)
- 🎨 **New Image Effects**: Add filters to `plugins/image_effects/`
- 📝 **Documentation**: Improve README, add examples
- 🐛 **Bug Fixes**: Check Issues tab for bugs
- 🧪 **Tests**: Add unit tests for existing features

### Advanced Contributions
- 🔌 **New Plugins**: Create entirely new plugin types
- 🖥️ **GUI Improvements**: Enhance PyQt5 interface
- ⚡ **Performance**: Optimize image processing
- 🌐 **Internationalization**: Add multi-language support

## 📋 Contribution Process

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 2. Make Your Changes
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Include tests for new features
- Update documentation if needed

### 3. Test Your Changes
```bash
# Run full test suite
pytest

# Test GUI functionality
python main.py --gui pyqt5
python main.py --gui tkinter
```

### 4. Commit & Push
```bash
git add .
git commit -m "✨ Add your feature description"
git push origin feature/your-feature-name
```

### 5. Create Pull Request
- Go to GitHub and create a Pull Request
- Describe what your changes do
- Link to relevant issues
- Wait for review and feedback

## 🎯 Plugin Development

### Creating a New Image Effect Plugin

1. **Create Plugin Directory**:
   ```
   plugins/my_effect/
   ├── manifest.json
   └── main.py
   ```

2. **Define Manifest**:
   ```json
   {
     "name": "My Effect",
     "version": "1.0.0",
     "description": "My custom image effect",
     "author": "Your Name",
     "main_module": "main",
     "plugin_class": "MyEffectPlugin"
   }
   ```

3. **Implement Plugin**:
   ```python
   from src.plugin_system import ImageProcessorPlugin
   
   class MyEffectPlugin(ImageProcessorPlugin):
       def process_image(self, image_path: str, **kwargs) -> str:
           # Your effect logic here
           return processed_image_path
   ```

## 📝 Code Style Guidelines

- **Python**: Follow PEP 8
- **Imports**: Group standard, third-party, local imports
- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain complex logic, not obvious code
- **Type Hints**: Use type hints for new functions

### Example:
```python
def process_image(self, image_path: str, quality: int = 85) -> str:
    """
    Process an image with specified quality.
    
    Args:
        image_path: Path to input image file
        quality: Compression quality (1-100)
        
    Returns:
        Path to processed image file
        
    Raises:
        ValueError: If quality is not in valid range
    """
    if not 1 <= quality <= 100:
        raise ValueError("Quality must be between 1 and 100")
    # ... processing logic
```

## 🐛 Bug Reports

When reporting bugs, please include:

- **OS and Python version**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Error messages (full traceback)**
- **Sample images (if relevant)**

## 💡 Feature Requests

For new features, please provide:

- **Use case description**
- **Proposed implementation approach**
- **UI mockups (for GUI features)**
- **Backward compatibility considerations**

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors graph

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs/features
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: All PRs get reviewed for quality

---

Thank you for contributing to Image-to-PDF Organizer! 🚀
