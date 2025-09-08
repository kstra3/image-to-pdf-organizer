"""
Image handling services for the Image-to-PDF Organizer.

This module provides functionality for handling, manipulating,
and processing images before they are converted to PDF.
"""

import os
from PIL import Image
from typing import List, Tuple, Optional


class ImageHandler:
    """Class for handling image operations."""

    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']

    @staticmethod
    def is_valid_image(file_path: str) -> bool:
        """
        Check if a file is a valid image format.

        Args:
            file_path: Path to the image file

        Returns:
            bool: True if the file is a valid image, False otherwise
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in ImageHandler.SUPPORTED_FORMATS

    @staticmethod
    def get_image_dimensions(file_path: str) -> Tuple[int, int]:
        """
        Get the dimensions of an image.

        Args:
            file_path: Path to the image file

        Returns:
            Tuple[int, int]: Width and height of the image
        """
        with Image.open(file_path) as img:
            return img.size

    @staticmethod
    def resize_image(file_path: str, size: Tuple[int, int], 
                     output_path: Optional[str] = None) -> str:
        """
        Resize an image to the specified dimensions.

        Args:
            file_path: Path to the image file
            size: Tuple of (width, height) for the new size
            output_path: Path to save the resized image (if None, overwrites original)

        Returns:
            str: Path to the resized image
        """
        if output_path is None:
            output_path = file_path

        with Image.open(file_path) as img:
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(output_path)

        return output_path

    @staticmethod
    def compress_image(file_path: str, quality: int = 85, 
                       output_path: Optional[str] = None) -> str:
        """
        Compress an image by reducing its quality.

        Args:
            file_path: Path to the image file
            quality: Quality level (1-100, lower means more compression)
            output_path: Path to save the compressed image (if None, overwrites original)

        Returns:
            str: Path to the compressed image
        """
        if output_path is None:
            output_path = file_path

        ext = os.path.splitext(file_path)[1].lower()
        
        # For PNG, we need to convert to RGB if it has transparency
        with Image.open(file_path) as img:
            if ext == '.png' and img.mode == 'RGBA':
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
                background.save(output_path, quality=quality, optimize=True)
            else:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, quality=quality, optimize=True)

        return output_path
