"""
Application settings and configuration management.
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class PDFSettings:
    """PDF conversion settings."""
    default_page_size: str = "A4"
    default_compression: bool = True
    default_quality: int = 85
    fit_to_page: bool = True
    maintain_aspect_ratio: bool = True


@dataclass
class ImageSettings:
    """Image processing settings."""
    max_width: int = 2048
    max_height: int = 2048
    auto_enhance: bool = False
    auto_rotate: bool = True
    remove_metadata: bool = False
    supported_formats: list = None
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']


@dataclass
class GUISettings:
    """GUI appearance and behavior settings."""
    theme: str = "dark"  # dark, light, auto
    window_width: int = 1000
    window_height: int = 700
    remember_window_position: bool = True
    last_window_x: int = 100
    last_window_y: int = 100
    show_image_previews: bool = True
    thumbnail_size: int = 150
    remember_last_directory: bool = True
    last_input_directory: str = ""
    last_output_directory: str = ""


@dataclass
class AppSettings:
    """Main application settings."""
    # Version info
    app_version: str = "2.0.0"
    config_version: str = "1.0"
    
    # Feature flags
    enable_advanced_features: bool = True
    enable_batch_processing: bool = True
    enable_project_management: bool = True
    enable_image_enhancement: bool = True
    
    # Performance settings
    max_concurrent_operations: int = 4
    memory_limit_mb: int = 512
    temp_directory: str = ""
    
    # Logging settings
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    log_to_file: bool = False
    log_file_path: str = "app.log"
    max_log_files: int = 5
    
    # Auto-update settings
    check_for_updates: bool = True
    auto_download_updates: bool = False
    
    # Sub-settings
    pdf: PDFSettings = None
    image: ImageSettings = None
    gui: GUISettings = None
    
    def __post_init__(self):
        if self.pdf is None:
            self.pdf = PDFSettings()
        if self.image is None:
            self.image = ImageSettings()
        if self.gui is None:
            self.gui = GUISettings()
        if not self.temp_directory:
            self.temp_directory = str(Path.home() / "AppData" / "Local" / "Temp" / "PDFOrganizer")


class SettingsManager:
    """Manages application settings with file persistence."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize settings manager.
        
        Args:
            config_dir: Custom configuration directory
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Default to user's app data directory
            if os.name == 'nt':  # Windows
                app_data = Path.home() / "AppData" / "Roaming"
            else:  # Unix-like
                app_data = Path.home() / ".config"
            
            self.config_dir = app_data / "PDFOrganizer"
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "settings.json"
        self.backup_file = self.config_dir / "settings.backup.json"
        
        self._settings: Optional[AppSettings] = None
    
    def load_settings(self) -> AppSettings:
        """Load settings from file or create defaults."""
        if self._settings is not None:
            return self._settings
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validate config version
                config_version = data.get('config_version', '1.0')
                if config_version != '1.0':
                    print(f"Warning: Config version mismatch. Expected 1.0, got {config_version}")
                
                # Create settings from data
                self._settings = self._dict_to_settings(data)
                
                # Migrate settings if needed
                if self._settings.config_version != '1.0':
                    self._migrate_settings()
                
            else:
                # Create default settings
                self._settings = AppSettings()
                self.save_settings()
        
        except Exception as e:
            print(f"Error loading settings: {e}")
            # Try to load backup
            if self.backup_file.exists():
                try:
                    print("Attempting to load backup settings...")
                    with open(self.backup_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self._settings = self._dict_to_settings(data)
                except Exception:
                    print("Backup settings also corrupted, using defaults")
                    self._settings = AppSettings()
            else:
                print("Using default settings")
                self._settings = AppSettings()
        
        return self._settings
    
    def save_settings(self) -> bool:
        """
        Save current settings to file.
        
        Returns:
            bool: True if saved successfully
        """
        if self._settings is None:
            return False
        
        try:
            # Create backup of current settings
            if self.config_file.exists():
                import shutil
                shutil.copy2(self.config_file, self.backup_file)
            
            # Convert settings to dict
            data = self._settings_to_dict(self._settings)
            
            # Save to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_settings(self) -> AppSettings:
        """Get current settings (load if not already loaded)."""
        return self.load_settings()
    
    def update_settings(self, **kwargs) -> bool:
        """
        Update specific settings.
        
        Args:
            **kwargs: Settings to update
            
        Returns:
            bool: True if updated successfully
        """
        settings = self.get_settings()
        
        try:
            for key, value in kwargs.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
                else:
                    # Handle nested settings
                    if '.' in key:
                        parts = key.split('.', 1)
                        sub_obj = getattr(settings, parts[0], None)
                        if sub_obj and hasattr(sub_obj, parts[1]):
                            setattr(sub_obj, parts[1], value)
            
            return self.save_settings()
            
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """
        Reset all settings to defaults.
        
        Returns:
            bool: True if reset successfully
        """
        try:
            self._settings = AppSettings()
            return self.save_settings()
        except Exception as e:
            print(f"Error resetting settings: {e}")
            return False
    
    def export_settings(self, export_path: str) -> bool:
        """
        Export settings to a file.
        
        Args:
            export_path: Path to export settings to
            
        Returns:
            bool: True if exported successfully
        """
        try:
            settings = self.get_settings()
            data = self._settings_to_dict(settings)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, import_path: str) -> bool:
        """
        Import settings from a file.
        
        Args:
            import_path: Path to import settings from
            
        Returns:
            bool: True if imported successfully
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._settings = self._dict_to_settings(data)
            return self.save_settings()
            
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
    
    def _dict_to_settings(self, data: Dict[str, Any]) -> AppSettings:
        """Convert dictionary to AppSettings object."""
        # Extract nested settings
        pdf_data = data.pop('pdf', {})
        image_data = data.pop('image', {})
        gui_data = data.pop('gui', {})
        
        # Create sub-settings
        pdf_settings = PDFSettings(**pdf_data) if pdf_data else PDFSettings()
        image_settings = ImageSettings(**image_data) if image_data else ImageSettings()
        gui_settings = GUISettings(**gui_data) if gui_data else GUISettings()
        
        # Create main settings
        settings = AppSettings(**data)
        settings.pdf = pdf_settings
        settings.image = image_settings
        settings.gui = gui_settings
        
        return settings
    
    def _settings_to_dict(self, settings: AppSettings) -> Dict[str, Any]:
        """Convert AppSettings object to dictionary."""
        data = asdict(settings)
        return data
    
    def _migrate_settings(self):
        """Migrate settings from older versions."""
        # Add migration logic here as needed
        pass
    
    def get_temp_directory(self) -> Path:
        """Get the temporary directory for the application."""
        temp_dir = Path(self.get_settings().temp_directory)
        temp_dir.mkdir(parents=True, exist_ok=True)
        return temp_dir
    
    def cleanup_temp_directory(self):
        """Clean up temporary files."""
        try:
            temp_dir = self.get_temp_directory()
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Error cleaning up temp directory: {e}")


# Global settings instance
_settings_manager = None


def get_settings_manager() -> SettingsManager:
    """Get the global settings manager instance."""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager


def get_settings() -> AppSettings:
    """Get application settings."""
    return get_settings_manager().get_settings()


def save_settings() -> bool:
    """Save application settings."""
    return get_settings_manager().save_settings()


def update_setting(key: str, value: Any) -> bool:
    """Update a specific setting."""
    return get_settings_manager().update_settings(**{key: value})


# Settings presets
PRESETS = {
    'performance': {
        'pdf.default_compression': True,
        'pdf.default_quality': 75,
        'image.max_width': 1920,
        'image.max_height': 1920,
        'max_concurrent_operations': 6,
    },
    'quality': {
        'pdf.default_compression': False,
        'pdf.default_quality': 95,
        'image.max_width': 4096,
        'image.max_height': 4096,
        'max_concurrent_operations': 2,
    },
    'minimal': {
        'enable_advanced_features': False,
        'enable_batch_processing': False,
        'enable_image_enhancement': False,
        'gui.show_image_previews': False,
        'memory_limit_mb': 256,
    }
}


def apply_preset(preset_name: str) -> bool:
    """Apply a settings preset."""
    if preset_name not in PRESETS:
        return False
    
    preset = PRESETS[preset_name]
    return get_settings_manager().update_settings(**preset)
