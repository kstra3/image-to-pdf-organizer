"""
Main entry point for the Image-to-PDF Organizer application.

This module determines whether to run the CLI or GUI interface
based on the command-line arguments provided.
"""

import sys
import argparse


def main():
    """Determine which interface to run and start the application."""
    parser = argparse.ArgumentParser(
        description='Image-to-PDF Organizer',
        add_help=False  # We'll add our own help to avoid conflicts with subcommands
    )
    
    parser.add_argument(
        '--gui',
        choices=['tkinter', 'qt'],
        default=None,
        help='Start the graphical user interface (tkinter or qt)'
    )
    
    parser.add_argument(
        '--qt',
        action='store_true',
        help='Start the advanced PyQt5 GUI (shortcut for --gui qt)'
    )
    
    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show this help message and exit'
    )
    
    # Parse only the known arguments to check for --gui flag
    args, remaining = parser.parse_known_args()
    
    if args.help and not args.gui and not args.qt and not remaining:
        parser.print_help()
        sys.exit(0)
    
    if args.qt or args.gui == 'qt':
        # Start the advanced PyQt5 GUI
        try:
            # Try to set Qt plugin path environment variable
            import os
            qt_plugin_path = os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins')
            if os.path.exists(qt_plugin_path):
                os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
            
            from src.gui.gui_2 import main as qt_main
            qt_main()
        except ImportError as e:
            print(f"PyQt5 is not installed properly: {e}")
            print("Falling back to basic Tkinter GUI...")
            from src.gui.app import main as gui_main
            gui_main()
        except Exception as e:
            print(f"PyQt5 GUI failed to start: {e}")
            print("This might be due to missing Qt platform plugins.")
            print("Falling back to basic Tkinter GUI...")
            from src.gui.app import main as gui_main
            gui_main()
    elif args.gui == 'tkinter' or (args.gui is not None and args.gui != 'qt'):
        # Start the basic Tkinter GUI
        from src.gui.app import main as gui_main
        gui_main()
    else:
        # Start the CLI with the remaining arguments
        sys.argv = [sys.argv[0]] + remaining
        from src.cli import main as cli_main
        cli_main()


if __name__ == '__main__':
    main()
