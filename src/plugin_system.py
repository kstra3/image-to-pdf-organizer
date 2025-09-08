"""
Plugin system for extending application functionality.
"""

import os
import sys
import importlib
import inspect
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Type
from pathlib import Path
import json


class PluginInterface(ABC):
    """Base interface for all plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass
    
    @property
    @abstractmethod
    def author(self) -> str:
        """Plugin author."""
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """Cleanup when plugin is unloaded."""
        pass


class ImageProcessorPlugin(PluginInterface):
    """Base class for image processing plugins."""
    
    @abstractmethod
    def process_image(self, image_path: str, **kwargs) -> str:
        """
        Process an image and return the path to the processed image.
        
        Args:
            image_path: Path to the input image
            **kwargs: Additional parameters
            
        Returns:
            str: Path to the processed image
        """
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Get plugin parameters schema."""
        pass


class PDFProcessorPlugin(PluginInterface):
    """Base class for PDF processing plugins."""
    
    @abstractmethod
    def process_pdf(self, pdf_path: str, **kwargs) -> str:
        """
        Process a PDF and return the path to the processed PDF.
        
        Args:
            pdf_path: Path to the input PDF
            **kwargs: Additional parameters
            
        Returns:
            str: Path to the processed PDF
        """
        pass


class UIPlugin(PluginInterface):
    """Base class for UI extension plugins."""
    
    @abstractmethod
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Get menu items to add to the application."""
        pass
    
    @abstractmethod
    def get_toolbar_items(self) -> List[Dict[str, Any]]:
        """Get toolbar items to add to the application."""
        pass


class PluginMetadata:
    """Plugin metadata container."""
    
    def __init__(self, manifest_path: str):
        """
        Initialize from manifest file.
        
        Args:
            manifest_path: Path to plugin manifest file
        """
        self.manifest_path = manifest_path
        self.plugin_dir = os.path.dirname(manifest_path)
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    @property
    def name(self) -> str:
        return self.data.get('name', '')
    
    @property
    def version(self) -> str:
        return self.data.get('version', '1.0.0')
    
    @property
    def description(self) -> str:
        return self.data.get('description', '')
    
    @property
    def author(self) -> str:
        return self.data.get('author', '')
    
    @property
    def main_module(self) -> str:
        return self.data.get('main_module', 'main')
    
    @property
    def plugin_class(self) -> str:
        return self.data.get('plugin_class', 'Plugin')
    
    @property
    def dependencies(self) -> List[str]:
        return self.data.get('dependencies', [])
    
    @property
    def min_app_version(self) -> str:
        return self.data.get('min_app_version', '1.0.0')
    
    @property
    def enabled(self) -> bool:
        return self.data.get('enabled', True)


class PluginManager:
    """Manages plugin loading, unloading, and execution."""
    
    def __init__(self, plugin_directories: List[str] = None):
        """
        Initialize plugin manager.
        
        Args:
            plugin_directories: List of directories to search for plugins
        """
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_metadata: Dict[str, PluginMetadata] = {}
        self.plugin_directories = plugin_directories or []
        self.hooks: Dict[str, List[Callable]] = {}
        
        # Add default plugin directory
        default_plugin_dir = os.path.join(os.path.dirname(__file__), '..', 'plugins')
        if os.path.exists(default_plugin_dir):
            self.plugin_directories.append(default_plugin_dir)
    
    def discover_plugins(self) -> List[PluginMetadata]:
        """
        Discover all available plugins.
        
        Returns:
            List[PluginMetadata]: List of discovered plugin metadata
        """
        discovered = []
        
        for directory in self.plugin_directories:
            if not os.path.exists(directory):
                continue
            
            for item in os.listdir(directory):
                plugin_path = os.path.join(directory, item)
                if not os.path.isdir(plugin_path):
                    continue
                
                manifest_path = os.path.join(plugin_path, 'manifest.json')
                if os.path.exists(manifest_path):
                    try:
                        metadata = PluginMetadata(manifest_path)
                        discovered.append(metadata)
                        self.plugin_metadata[metadata.name] = metadata
                    except Exception as e:
                        print(f"Error loading plugin manifest {manifest_path}: {e}")
        
        return discovered
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        Load a specific plugin.
        
        Args:
            plugin_name: Name of the plugin to load
            
        Returns:
            bool: True if loaded successfully
        """
        if plugin_name in self.plugins:
            print(f"Plugin {plugin_name} is already loaded")
            return True
        
        if plugin_name not in self.plugin_metadata:
            print(f"Plugin {plugin_name} not found")
            return False
        
        metadata = self.plugin_metadata[plugin_name]
        
        if not metadata.enabled:
            print(f"Plugin {plugin_name} is disabled")
            return False
        
        try:
            # Add plugin directory to Python path
            if metadata.plugin_dir not in sys.path:
                sys.path.insert(0, metadata.plugin_dir)
            
            # Import the plugin module
            module = importlib.import_module(metadata.main_module)
            
            # Get the plugin class
            plugin_class = getattr(module, metadata.plugin_class)
            
            # Verify it implements the correct interface
            if not issubclass(plugin_class, PluginInterface):
                raise ValueError(f"Plugin class must inherit from PluginInterface")
            
            # Create plugin instance
            plugin_instance = plugin_class()
            
            # Initialize the plugin
            if not plugin_instance.initialize():
                raise RuntimeError("Plugin initialization failed")
            
            # Store the plugin
            self.plugins[plugin_name] = plugin_instance
            
            print(f"Plugin {plugin_name} loaded successfully")
            return True
            
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a specific plugin.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            bool: True if unloaded successfully
        """
        if plugin_name not in self.plugins:
            print(f"Plugin {plugin_name} is not loaded")
            return True
        
        try:
            plugin = self.plugins[plugin_name]
            
            # Cleanup the plugin
            plugin.cleanup()
            
            # Remove from loaded plugins
            del self.plugins[plugin_name]
            
            print(f"Plugin {plugin_name} unloaded successfully")
            return True
            
        except Exception as e:
            print(f"Error unloading plugin {plugin_name}: {e}")
            return False
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload a plugin.
        
        Args:
            plugin_name: Name of the plugin to reload
            
        Returns:
            bool: True if reloaded successfully
        """
        if not self.unload_plugin(plugin_name):
            return False
        return self.load_plugin(plugin_name)
    
    def load_all_plugins(self) -> Dict[str, bool]:
        """
        Load all discovered plugins.
        
        Returns:
            Dict[str, bool]: Plugin name to success status mapping
        """
        self.discover_plugins()
        results = {}
        
        for plugin_name in self.plugin_metadata:
            results[plugin_name] = self.load_plugin(plugin_name)
        
        return results
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """
        Get a loaded plugin instance.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Optional[PluginInterface]: Plugin instance or None
        """
        return self.plugins.get(plugin_name)
    
    def get_plugins_by_type(self, plugin_type: Type[PluginInterface]) -> List[PluginInterface]:
        """
        Get all loaded plugins of a specific type.
        
        Args:
            plugin_type: Plugin type to filter by
            
        Returns:
            List[PluginInterface]: List of matching plugins
        """
        return [plugin for plugin in self.plugins.values() 
                if isinstance(plugin, plugin_type)]
    
    def register_hook(self, hook_name: str, callback: Callable) -> bool:
        """
        Register a hook callback.
        
        Args:
            hook_name: Name of the hook
            callback: Callback function
            
        Returns:
            bool: True if registered successfully
        """
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        
        if callback not in self.hooks[hook_name]:
            self.hooks[hook_name].append(callback)
            return True
        
        return False
    
    def unregister_hook(self, hook_name: str, callback: Callable) -> bool:
        """
        Unregister a hook callback.
        
        Args:
            hook_name: Name of the hook
            callback: Callback function
            
        Returns:
            bool: True if unregistered successfully
        """
        if hook_name in self.hooks and callback in self.hooks[hook_name]:
            self.hooks[hook_name].remove(callback)
            return True
        
        return False
    
    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Execute all callbacks for a hook.
        
        Args:
            hook_name: Name of the hook
            *args: Positional arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
            
        Returns:
            List[Any]: List of results from callbacks
        """
        results = []
        
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Error executing hook {hook_name}: {e}")
        
        return results
    
    def get_plugin_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all plugins.
        
        Returns:
            List[Dict[str, Any]]: List of plugin information
        """
        info = []
        
        for name, metadata in self.plugin_metadata.items():
            plugin_info = {
                'name': metadata.name,
                'version': metadata.version,
                'description': metadata.description,
                'author': metadata.author,
                'enabled': metadata.enabled,
                'loaded': name in self.plugins,
                'path': metadata.plugin_dir
            }
            
            if name in self.plugins:
                plugin = self.plugins[name]
                plugin_info['type'] = type(plugin).__name__
            
            info.append(plugin_info)
        
        return info


# Global plugin manager instance
_plugin_manager = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


def load_plugins():
    """Load all available plugins."""
    manager = get_plugin_manager()
    results = manager.load_all_plugins()
    
    loaded_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print(f"Loaded {loaded_count}/{total_count} plugins")


def get_image_processors() -> List[ImageProcessorPlugin]:
    """Get all loaded image processor plugins."""
    manager = get_plugin_manager()
    return manager.get_plugins_by_type(ImageProcessorPlugin)


def get_pdf_processors() -> List[PDFProcessorPlugin]:
    """Get all loaded PDF processor plugins."""
    manager = get_plugin_manager()
    return manager.get_plugins_by_type(PDFProcessorPlugin)


def get_ui_plugins() -> List[UIPlugin]:
    """Get all loaded UI plugins."""
    manager = get_plugin_manager()
    return manager.get_plugins_by_type(UIPlugin)
