"""
Smart GUI Launcher for Image-to-PDF Organizer.

This module automatically detects the best available GUI and provides
a seamless fallback system.
"""

import sys
import os
from typing import Optional


class GUILauncher:
    """Smart GUI launcher with automatic fallback."""
    
    @staticmethod
    def detect_available_guis():
        """Detect which GUI frameworks are available."""
        available = {
            'tkinter': False,
            'pyqt5': False,
            'pyside2': False  # Future alternative
        }
        
        # Test Tkinter
        try:
            import tkinter
            available['tkinter'] = True
        except ImportError:
            pass
        
        # Test PyQt5
        try:
            from PyQt5.QtWidgets import QApplication
            # Test if Qt platform plugins are available
            test_app = QApplication.instance() or QApplication([])
            available['pyqt5'] = True
        except Exception:
            pass
        
        # Test PySide2 (future alternative)
        try:
            from PySide2.QtWidgets import QApplication
            available['pyside2'] = True
        except ImportError:
            pass
            
        return available
    
    @staticmethod
    def fix_qt_plugin_path():
        """Try to fix Qt plugin path issues on Windows."""
        if sys.platform != 'win32':
            return
            
        import os
        
        # Common PyQt5 plugin paths
        possible_paths = [
            os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'),
            os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt', 'plugins'),
            os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'),
            os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages', 'PyQt5', 'Qt', 'plugins'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                os.environ['QT_PLUGIN_PATH'] = path
                print(f"Set QT_PLUGIN_PATH to: {path}")
                return True
        
        return False
    
    def launch_gui(self, framework: str):
        """Launch a specific GUI framework."""
        if framework == 'pyqt5' or framework == 'qt':
            return self._launch_pyqt5_gui()
        elif framework == 'tkinter':
            return self._launch_tkinter_gui()
        elif framework == 'auto':
            return self.detect_best_gui()
        else:
            raise ValueError(f"Unknown GUI framework: {framework}")
    
    def _launch_pyqt5_gui(self):
        """Launch PyQt5 GUI with error handling."""
        try:
            print("🚀 Starting advanced PyQt5 GUI...")
            self.fix_qt_plugin_path()
            from src.gui.gui_2 import main as qt_main
            return qt_main()
        except ImportError as e:
            print(f"❌ PyQt5 not available: {e}")
            raise
        except Exception as e:
            print(f"❌ PyQt5 GUI failed: {e}")
            raise
    
    def _launch_tkinter_gui(self):
        """Launch Tkinter GUI with error handling."""
        try:
            print("🚀 Starting basic Tkinter GUI...")
            from src.gui.app import main as gui_main
            return gui_main()
        except ImportError as e:
            print(f"❌ Tkinter not available: {e}")
            raise
        except Exception as e:
            print(f"❌ Tkinter GUI failed: {e}")
            raise
    
    def detect_best_gui(self):
        """Detect and launch the best available GUI."""
        available = self.detect_available_guis()
        
        print("🔍 Detecting available GUI frameworks...")
        for framework, is_available in available.items():
            status = "✅ Available" if is_available else "❌ Not available"
            print(f"  {framework.upper()}: {status}")
        
        # Try PyQt5 first (advanced GUI)
        if available['pyqt5']:
            try:
                return self._launch_pyqt5_gui()
            except Exception as e:
                print(f"❌ PyQt5 GUI failed: {e}")
                print("🔄 Falling back to Tkinter...")
        
        # Fallback to Tkinter
        if available['tkinter']:
            try:
                return self._launch_tkinter_gui()
            except Exception as e:
                print(f"❌ Tkinter GUI failed: {e}")
        
        # If all GUIs fail
        print("❌ No GUI framework is available!")
        print("Please install one of the following:")
        print("  - For basic GUI: Tkinter (usually included with Python)")
        print("  - For advanced GUI: pip install PyQt5")
        raise RuntimeError("No GUI frameworks available")
    
    @staticmethod
    def launch_best_gui(preferred: Optional[str] = None):
        """Launch the best available GUI (static method for backward compatibility)."""
        launcher = GUILauncher()
        
        if preferred:
            try:
                return launcher.launch_gui(preferred)
            except Exception:
                print(f"🔄 Preferred GUI '{preferred}' failed, trying auto-detection...")
        
        return launcher.detect_best_gui()


def main():
    """Main GUI launcher function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Launch Image-to-PDF Organizer GUI")
    parser.add_argument('--prefer', choices=['tkinter', 'qt'], help='Preferred GUI framework')
    
    args = parser.parse_args()
    
    GUILauncher.launch_best_gui(preferred=args.prefer)


if __name__ == '__main__':
    main()
