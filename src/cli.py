"""
Command-line interface for the Image-to-PDF Organizer.

This module provides a command-line interface for converting 
images to PDF with various options and configurations.
"""

import os
import argparse
from typing import List
import sys
from src.services.image_handler import ImageHandler
from src.services.pdf_converter import PDFConverter


def progress_callback(progress: float) -> None:
    """
    Display a progress bar in the console.
    
    Args:
        progress: Progress value between 0 and 1
    """
    bar_length = 40
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percent = int(100 * progress)
    print(f'\rProgress: |{bar}| {percent}%', end='')
    if progress >= 1:
        print()


def validate_images(image_paths: List[str]) -> List[str]:
    """
    Validate that all provided paths are valid images.
    
    Args:
        image_paths: List of image file paths
    
    Returns:
        List[str]: List of valid image paths
    """
    valid_images = []
    
    for path in image_paths:
        if not os.path.exists(path):
            print(f"Warning: File not found: {path}")
            continue
            
        if not ImageHandler.is_valid_image(path):
            print(f"Warning: Unsupported file format: {path}")
            continue
            
        valid_images.append(path)
    
    return valid_images


def main():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(
        description='Convert multiple images to a single PDF file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        'images', 
        nargs='+', 
        help='Paths to image files (JPG, PNG, etc.)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output.pdf',
        help='Output PDF file path'
    )
    
    parser.add_argument(
        '-s', '--page-size',
        choices=['A4', 'LETTER', 'LEGAL', 'TABLOID', 'FIT'],
        default='A4',
        help='PDF page size (FIT uses original image dimensions)'
    )
    
    parser.add_argument(
        '-c', '--compress',
        action='store_true',
        help='Enable image compression to reduce PDF size'
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=85,
        choices=range(1, 101),
        metavar='[1-100]',
        help='Compression quality (1=highest compression, 100=best quality)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate image paths
    image_paths = validate_images(args.images)
    
    if not image_paths:
        print("Error: No valid images provided.")
        sys.exit(1)
    
    # Confirm the operation
    print(f"Converting {len(image_paths)} images to PDF...")
    print(f"Output file: {args.output}")
    print(f"Page size: {args.page_size}")
    print(f"Compression: {'Enabled' if args.compress else 'Disabled'}")
    if args.compress:
        print(f"Quality: {args.quality}")
    
    try:
        # Convert images to PDF
        converter = PDFConverter()
        output_path = converter.convert_images_to_pdf(
            image_paths=image_paths,
            output_path=args.output,
            page_size=args.page_size,
            compress=args.compress,
            compression_quality=args.quality,
            callback=progress_callback
        )
        
        print(f"\nPDF created successfully: {output_path}")
        print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
