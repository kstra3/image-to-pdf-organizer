"""
Enhanced main entry point with all new features integrated.
Image-to-PDF Organizer v2.0 - Professional Edition
"""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import components
from launcher import GUILauncher
from settings_manager import get_settings, get_settings_manager
from plugin_system import get_plugin_manager, load_plugins
from help_system import get_help_system, show_help, quick_help


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██████╗ ██████╗ ██████╗     ██████╗ ██████╗  ██████╗     ║
║    ██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗    ║
║    ██████╔╝██║  ██║█████╗      ██████╔╝██████╔╝██║   ██║    ║
║    ██╔═══╝ ██║  ██║██╔══╝      ██╔═══╝ ██╔══██╗██║   ██║    ║
║    ██║     ██████╔╝██║         ██║     ██║  ██║╚██████╔╝    ║
║    ╚═╝     ╚═════╝ ╚═╝         ╚═╝     ╚═╝  ╚═╝ ╚═════╝     ║
║                                                              ║
║           Image-to-PDF Organizer Professional               ║
║                      Version 2.0.0                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🚀 Advanced Features:
  • Dual GUI interfaces (Tkinter + PyQt5)
  • Professional CLI with progress indicators
  • Advanced image processing & enhancement
  • Project management system
  • Plugin architecture for extensibility
  • Comprehensive help system
  • Smart configuration management

📖 Quick Help: Use --help for options or --show-help for full documentation
"""
    print(banner)


def show_version():
    """Show version information."""
    settings = get_settings()
    print(f"""
Image-to-PDF Organizer Professional
Version: {settings.app_version}
Configuration Version: {settings.config_version}

Features Enabled:
  ✓ Advanced Features: {'Yes' if settings.enable_advanced_features else 'No'}
  ✓ Batch Processing: {'Yes' if settings.enable_batch_processing else 'No'}
  ✓ Project Management: {'Yes' if settings.enable_project_management else 'No'}
  ✓ Image Enhancement: {'Yes' if settings.enable_image_enhancement else 'No'}
  
System Information:
  • Python: {sys.version.split()[0]}
  • Platform: {sys.platform}
  • Working Directory: {os.getcwd()}
  • Settings Directory: {get_settings_manager().config_dir}
""")


def setup_logging():
    """Setup application logging."""
    import logging
    
    settings = get_settings()
    
    # Configure logging level
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # Configure format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(console_handler)
    
    # File handler if enabled
    if settings.log_to_file:
        try:
            log_file = Path(settings.log_file_path)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            logger.addHandler(file_handler)
            
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")


def initialize_application():
    """Initialize the application."""
    # Setup logging first
    setup_logging()
    
    # Load settings
    settings = get_settings()
    
    # Initialize plugin system if enabled
    if settings.enable_advanced_features:
        try:
            load_plugins()
        except Exception as e:
            print(f"Warning: Plugin system initialization failed: {e}")
    
    # Ensure temp directory exists
    get_settings_manager().get_temp_directory()


def main():
    """Enhanced main entry point."""
    parser = argparse.ArgumentParser(
        description='Image-to-PDF Organizer Professional v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Launch Modes:
  python main.py                    # Auto-detect best GUI
  python main.py --gui pyqt5        # Force advanced GUI
  python main.py --gui tkinter      # Force basic GUI
  python main.py --cli              # Enhanced command line
  python main.py --settings         # Settings management
  
Examples:
  python main.py                    # Launch with best available GUI
  python main.py --launcher         # Show smart launcher menu
  python main.py --version          # Show version information
  python main.py --help-topics      # List help topics
  python main.py --show-help        # Open full documentation
        """
    )
    
    # Launch options
    parser.add_argument(
        '--gui',
        choices=['auto', 'pyqt5', 'tkinter', 'none'],
        default='auto',
        help='GUI framework to use'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Launch enhanced command-line interface'
    )
    
    parser.add_argument(
        '--launcher',
        action='store_true',
        help='Show smart launcher menu'
    )
    
    # Information options
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )
    
    parser.add_argument(
        '--show-help',
        action='store_true',
        help='Open comprehensive help documentation'
    )
    
    parser.add_argument(
        '--help-topics',
        action='store_true',
        help='List available help topics'
    )
    
    parser.add_argument(
        '--quick-help',
        type=str,
        metavar='TOPIC',
        help='Get quick help for a topic'
    )
    
    # Management options
    parser.add_argument(
        '--settings',
        action='store_true',
        help='Open settings management'
    )
    
    parser.add_argument(
        '--reset-settings',
        action='store_true',
        help='Reset all settings to defaults'
    )
    
    parser.add_argument(
        '--plugins',
        action='store_true',
        help='Show plugin information'
    )
    
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='Cleanup temporary files and logs'
    )
    
    # Display options
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Skip banner display'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Set logging level'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle logging level override
    if args.log_level:
        import logging
        logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Initialize application
    initialize_application()
    
    # Handle version request
    if args.version:
        show_version()
        return
    
    # Handle help requests
    if args.show_help:
        show_help()
        return
    
    if args.help_topics:
        help_system = get_help_system()
        topics = help_system.list_topics()
        print("\nAvailable Help Topics:")
        print("=" * 50)
        for topic in topics:
            print(f"  {topic['id']:<20} {topic['title']}")
        print("\nUse --quick-help TOPIC for quick information")
        print("Use --show-help to open full documentation")
        return
    
    if args.quick_help:
        help_text = quick_help(args.quick_help)
        print(f"\nQuick Help - {args.quick_help}:")
        print("=" * 40)
        print(help_text)
        return
    
    # Handle management options
    if args.reset_settings:
        manager = get_settings_manager()
        if manager.reset_to_defaults():
            print("✅ Settings reset to defaults successfully")
        else:
            print("❌ Failed to reset settings")
        return
    
    if args.cleanup:
        manager = get_settings_manager()
        manager.cleanup_temp_directory()
        print("✅ Temporary files cleaned up")
        return
    
    if args.plugins:
        plugin_manager = get_plugin_manager()
        plugins = plugin_manager.get_plugin_info()
        
        if not plugins:
            print("No plugins found")
            return
        
        print("\nPlugin Information:")
        print("=" * 60)
        for plugin in plugins:
            status = "✅ Loaded" if plugin['loaded'] else "⚪ Available"
            print(f"{plugin['name']:<25} v{plugin['version']:<8} {status}")
            if plugin.get('description'):
                print(f"  {plugin['description']}")
            print()
        return
    
    # Show banner unless suppressed
    if not args.no_banner:
        print_banner()
    
    # Handle settings management
    if args.settings:
        try:
            from settings_gui import SettingsGUI
            settings_gui = SettingsGUI()
            settings_gui.run()
        except ImportError:
            print("Settings GUI not available. Use --reset-settings for command-line management.")
        return
    
    # Handle launcher menu
    if args.launcher:
        try:
            # Use the Windows batch launcher if available
            launcher_path = Path(__file__).parent / "smart_launcher.bat"
            if launcher_path.exists() and sys.platform == 'win32':
                os.system(str(launcher_path))
            else:
                # Fallback to Python launcher
                launcher = GUILauncher()
                result = launcher.show_launcher_menu()
                if result:
                    launcher.launch_gui(result)
        except Exception as e:
            print(f"Launcher error: {e}")
            args.gui = 'auto'  # Fall back to auto GUI
    
    # Handle CLI mode
    if args.cli:
        try:
            from cli_enhanced import main as cli_main
            # Remove our arguments and pass the rest to CLI
            cli_args = [arg for arg in sys.argv[1:] if not arg.startswith('--cli')]
            sys.argv = [sys.argv[0]] + cli_args
            cli_main()
        except ImportError:
            print("Enhanced CLI not available, falling back to basic CLI")
            try:
                from cli import main as basic_cli_main
                basic_cli_main()
            except ImportError:
                print("No CLI interface available")
        return
    
    # Handle GUI launch
    if args.gui != 'none':
        try:
            launcher = GUILauncher()
            
            if args.gui == 'auto':
                print("🎯 Auto-detecting best GUI interface...")
                launcher.detect_best_gui()
            else:
                print(f"🎯 Launching {args.gui.upper()} interface...")
                launcher.launch_gui(args.gui)
                
        except Exception as e:
            print(f"❌ GUI launch failed: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            
            # Try fallback
            print("🔄 Trying fallback options...")
            try:
                launcher = GUILauncher()
                print("🎯 Launching fallback interface...")
                launcher.detect_best_gui()
            except Exception:
                print("❌ All GUI options failed")
    else:
        print("No interface specified. Use --help for options.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
