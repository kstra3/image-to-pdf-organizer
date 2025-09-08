"""
Enhanced command-line interface with better UX and features.
"""

import os
import sys
import argparse
import time
from typing import List, Optional
from src.services.image_handler import ImageHandler
from src.services.pdf_converter import PDFConverter
from src.services.advanced_processor import AdvancedImageProcessor


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def disable():
        """Disable colors (for Windows compatibility)."""
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.MAGENTA = ''
        Colors.CYAN = ''
        Colors.WHITE = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''
        Colors.END = ''


def print_banner():
    """Print application banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╦╔╦╗╔═╗╔═╗╔═╗  ┌┬┐┌─┐  ╔═╗╔╦╗╔═╗  ╔═╗┬─┐┌─┐┌─┐┌┐┌┬┌─┐┌─┐┬─┐
║║║║╠═╣║ ╦║╣    │ │ │  ╠═╝ ║║╠╣   ║ ║├┬┘│ ┬├─┤││││┌─┘├┤ ├┬┘
╩╩ ╩╩ ╩╚═╝╚═╝   ┴ └─┘  ╩  ═╩╝╚    ╚═╝┴└─└─┘┴ ┴┘└┘┴└─┘└─┘┴└─
{Colors.END}
{Colors.YELLOW}                    Professional Image-to-PDF Conversion{Colors.END}
{Colors.WHITE}                              Version 2.0{Colors.END}
"""
    print(banner)


def print_progress_bar(progress: float, width: int = 50, 
                      label: str = "Progress", color: str = Colors.GREEN):
    """Print an animated progress bar."""
    filled = int(width * progress)
    bar = '█' * filled + '░' * (width - filled)
    percent = int(100 * progress)
    
    # Clear line and print progress
    sys.stdout.write(f'\r{color}{label}: |{bar}| {percent}%{Colors.END}')
    sys.stdout.flush()
    
    if progress >= 1:
        print()  # New line when complete


def validate_and_filter_images(image_paths: List[str], verbose: bool = True) -> List[str]:
    """Validate and filter image paths."""
    valid_images = []
    invalid_count = 0
    
    if verbose:
        print(f"\n{Colors.BLUE}🔍 Validating images...{Colors.END}")
    
    for i, path in enumerate(image_paths):
        if verbose and len(image_paths) > 10:
            print_progress_bar((i + 1) / len(image_paths), label="Validating")
        
        if not os.path.exists(path):
            if verbose:
                print(f"{Colors.RED}✗ File not found: {path}{Colors.END}")
            invalid_count += 1
            continue
            
        if not ImageHandler.is_valid_image(path):
            if verbose:
                print(f"{Colors.RED}✗ Invalid image format: {path}{Colors.END}")
            invalid_count += 1
            continue
            
        valid_images.append(path)
        if verbose and len(image_paths) <= 10:
            print(f"{Colors.GREEN}✓ {os.path.basename(path)}{Colors.END}")
    
    if verbose:
        if invalid_count > 0:
            print(f"{Colors.YELLOW}⚠️  Skipped {invalid_count} invalid files{Colors.END}")
        print(f"{Colors.GREEN}✅ Found {len(valid_images)} valid images{Colors.END}")
    
    return valid_images


def enhanced_progress_callback(stage: str):
    """Create a progress callback for a specific stage."""
    def callback(progress: float):
        print_progress_bar(progress, label=stage, color=Colors.CYAN)
    return callback


def main():
    """Enhanced command-line interface."""
    # Disable colors on Windows if not supported
    if sys.platform == 'win32':
        try:
            import colorama
            colorama.init()
        except ImportError:
            Colors.disable()
    
    parser = argparse.ArgumentParser(
        description='Image-to-PDF Organizer Pro - Enhanced CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.BOLD}Examples:{Colors.END}
  Basic conversion:
    %(prog)s photo1.jpg photo2.png -o album.pdf
    
  With compression and custom size:
    %(prog)s vacation/*.jpg -o vacation.pdf -s LETTER -c -q 80
    
  Batch processing with enhancements:
    %(prog)s *.png -o enhanced.pdf --enhance --auto-rotate
    
  Fit original image size:
    %(prog)s screenshot.png -o screenshot.pdf -s FIT

{Colors.BOLD}Supported formats:{Colors.END} JPG, JPEG, PNG, BMP, TIFF, GIF
        """
    )
    
    # Positional arguments
    parser.add_argument(
        'images', 
        nargs='+', 
        help='Image files to convert (supports wildcards)'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        default='output.pdf',
        help='Output PDF file path (default: output.pdf)'
    )
    
    # PDF options
    parser.add_argument(
        '-s', '--page-size',
        choices=['A4', 'LETTER', 'LEGAL', 'TABLOID', 'FIT'],
        default='A4',
        help='PDF page size (default: A4)'
    )
    
    # Compression options
    parser.add_argument(
        '-c', '--compress',
        action='store_true',
        help='Enable image compression'
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=85,
        choices=range(1, 101),
        metavar='[1-100]',
        help='Compression quality (default: 85)'
    )
    
    # Enhancement options
    parser.add_argument(
        '--enhance',
        action='store_true',
        help='Apply automatic image enhancement'
    )
    
    parser.add_argument(
        '--auto-rotate',
        action='store_true',
        help='Auto-rotate images based on EXIF data'
    )
    
    parser.add_argument(
        '--watermark',
        type=str,
        help='Add text watermark to images'
    )
    
    # Display options
    parser.add_argument(
        '--quiet', '-quiet',
        action='store_true',
        help='Minimal output (quiet mode)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Detailed output (verbose mode)'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Skip banner display'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set verbosity
    verbose = args.verbose and not args.quiet
    
    # Show banner unless suppressed
    if not args.no_banner and not args.quiet:
        print_banner()
    
    # Validate images
    if verbose or not args.quiet:
        print(f"{Colors.BLUE}📁 Processing {len(args.images)} file pattern(s)...{Colors.END}")
    
    # Expand wildcards and validate
    import glob
    expanded_paths = []
    for pattern in args.images:
        matches = glob.glob(pattern)
        if matches:
            expanded_paths.extend(matches)
        else:
            expanded_paths.append(pattern)  # Keep as-is if no matches
    
    image_paths = validate_and_filter_images(expanded_paths, verbose=verbose or not args.quiet)
    
    if not image_paths:
        print(f"{Colors.RED}❌ No valid images found!{Colors.END}")
        sys.exit(1)
    
    # Show conversion settings
    if not args.quiet:
        print(f"\n{Colors.BOLD}📋 Conversion Settings:{Colors.END}")
        print(f"  Output file: {Colors.CYAN}{args.output}{Colors.END}")
        print(f"  Page size: {Colors.CYAN}{args.page_size}{Colors.END}")
        print(f"  Compression: {Colors.GREEN if args.compress else Colors.RED}{'Enabled' if args.compress else 'Disabled'}{Colors.END}")
        if args.compress:
            print(f"  Quality: {Colors.CYAN}{args.quality}%{Colors.END}")
        if args.enhance:
            print(f"  Enhancement: {Colors.GREEN}Enabled{Colors.END}")
        if args.auto_rotate:
            print(f"  Auto-rotate: {Colors.GREEN}Enabled{Colors.END}")
        if args.watermark:
            print(f"  Watermark: {Colors.CYAN}{args.watermark}{Colors.END}")
        print()
    
    try:
        # Process images if enhancements are requested
        if args.enhance or args.auto_rotate or args.watermark:
            if not args.quiet:
                print(f"{Colors.YELLOW}🔧 Applying image enhancements...{Colors.END}")
            
            processor = AdvancedImageProcessor()
            processed_paths = []
            
            for i, img_path in enumerate(image_paths):
                if not args.quiet:
                    print_progress_bar((i + 1) / len(image_paths), label="Processing")
                
                current_path = img_path
                
                # Auto-rotate
                if args.auto_rotate:
                    current_path = processor.auto_rotate_image(current_path)
                
                # Enhance
                if args.enhance:
                    current_path = processor.enhance_image(current_path)
                
                # Watermark
                if args.watermark:
                    current_path = processor.add_text_watermark(current_path, args.watermark)
                
                processed_paths.append(current_path)
            
            image_paths = processed_paths
            
            if not args.quiet:
                print(f"{Colors.GREEN}✅ Image enhancement complete{Colors.END}")
        
        # Convert to PDF
        if not args.quiet:
            print(f"{Colors.MAGENTA}📄 Converting to PDF...{Colors.END}")
        
        start_time = time.time()
        
        converter = PDFConverter()
        
        # Create progress callback
        progress_callback = None
        if not args.quiet:
            progress_callback = enhanced_progress_callback("Converting")
        
        output_path = converter.convert_images_to_pdf(
            image_paths=image_paths,
            output_path=args.output,
            page_size=args.page_size,
            compress=args.compress,
            compression_quality=args.quality,
            callback=progress_callback
        )
        
        elapsed = time.time() - start_time
        
        # Show results
        if not args.quiet:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 SUCCESS!{Colors.END}")
            print(f"{Colors.GREEN}✅ PDF created: {output_path}{Colors.END}")
            
            # File info
            file_size = os.path.getsize(output_path) / 1024  # KB
            if file_size > 1024:
                size_str = f"{file_size/1024:.1f} MB"
            else:
                size_str = f"{file_size:.1f} KB"
                
            print(f"{Colors.WHITE}📊 File size: {size_str}{Colors.END}")
            print(f"{Colors.WHITE}⏱️  Time taken: {elapsed:.1f} seconds{Colors.END}")
            print(f"{Colors.WHITE}📸 Images processed: {len(image_paths)}{Colors.END}")
        else:
            # Quiet mode - just print the output path
            print(output_path)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Operation cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
