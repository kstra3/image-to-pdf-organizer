"""
Enhanced image processing service with advanced features.

This module extends the basic image handler with more advanced
image processing capabilities like rotation, watermarking, and optimization.
"""

import os
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from typing import List, Tuple, Optional, Union
import logging


class AdvancedImageProcessor:
    """Advanced image processing with additional features."""
    
    def __init__(self):
        """Initialize the advanced image processor."""
        self.temp_dir = tempfile.mkdtemp()
        self.logger = logging.getLogger(__name__)
    
    def auto_rotate_image(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        Auto-rotate image based on EXIF orientation data.
        
        Args:
            image_path: Path to input image
            output_path: Path to save rotated image (optional)
            
        Returns:
            str: Path to processed image
        """
        if output_path is None:
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_rotated{ext}"
        
        try:
            with Image.open(image_path) as img:
                # Check for EXIF orientation
                exif = img._getexif() if hasattr(img, '_getexif') else None
                if exif:
                    orientation = exif.get(0x0112)  # Orientation tag
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
                
                img.save(output_path)
                return output_path
                
        except Exception as e:
            self.logger.warning(f"Auto-rotation failed for {image_path}: {e}")
            # If rotation fails, just copy the original
            if output_path != image_path:
                import shutil
                shutil.copy2(image_path, output_path)
            return output_path
    
    def add_text_watermark(self, image_path: str, watermark_text: str,
                          position: str = 'bottom-right', opacity: float = 0.7,
                          font_size: int = 36, output_path: Optional[str] = None) -> str:
        """
        Add text watermark to image.
        
        Args:
            image_path: Path to input image
            watermark_text: Text to add as watermark
            position: Position of watermark ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
            opacity: Opacity of watermark (0.0 to 1.0)
            font_size: Size of watermark font
            output_path: Path to save watermarked image (optional)
            
        Returns:
            str: Path to watermarked image
        """
        if output_path is None:
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_watermarked{ext}"
        
        with Image.open(image_path) as img:
            # Convert to RGBA to support transparency
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a transparent overlay
            overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Try to use a good font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except (OSError, IOError):
                font = ImageFont.load_default()
            
            # Get text size
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position
            img_width, img_height = img.size
            margin = 20
            
            if position == 'top-left':
                x, y = margin, margin
            elif position == 'top-right':
                x, y = img_width - text_width - margin, margin
            elif position == 'bottom-left':
                x, y = margin, img_height - text_height - margin
            elif position == 'bottom-right':
                x, y = img_width - text_width - margin, img_height - text_height - margin
            elif position == 'center':
                x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
            else:
                x, y = img_width - text_width - margin, img_height - text_height - margin
            
            # Draw text with semi-transparency
            alpha = int(255 * opacity)
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, alpha))
            
            # Composite the overlay onto the original image
            watermarked = Image.alpha_composite(img, overlay)
            
            # Convert back to RGB if needed
            if watermarked.mode == 'RGBA':
                background = Image.new('RGB', watermarked.size, (255, 255, 255))
                background.paste(watermarked, mask=watermarked.split()[3])
                watermarked = background
            
            watermarked.save(output_path)
            return output_path
    
    def enhance_image(self, image_path: str, brightness: float = 1.0,
                     contrast: float = 1.0, saturation: float = 1.0,
                     sharpness: float = 1.0, output_path: Optional[str] = None) -> str:
        """
        Enhance image with brightness, contrast, saturation, and sharpness adjustments.
        
        Args:
            image_path: Path to input image
            brightness: Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)
            contrast: Contrast factor (1.0 = no change)
            saturation: Saturation factor (1.0 = no change)
            sharpness: Sharpness factor (1.0 = no change)
            output_path: Path to save enhanced image (optional)
            
        Returns:
            str: Path to enhanced image
        """
        if output_path is None:
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_enhanced{ext}"
        
        with Image.open(image_path) as img:
            # Apply enhancements
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
            
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation)
            
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(sharpness)
            
            img.save(output_path)
            return output_path
    
    def create_thumbnail_grid(self, image_paths: List[str], grid_size: Tuple[int, int],
                             thumbnail_size: Tuple[int, int] = (200, 200),
                             output_path: Optional[str] = None) -> str:
        """
        Create a grid of thumbnails from multiple images.
        
        Args:
            image_paths: List of image file paths
            grid_size: Grid dimensions (cols, rows)
            thumbnail_size: Size of each thumbnail
            output_path: Path to save grid image
            
        Returns:
            str: Path to grid image
        """
        if output_path is None:
            output_path = os.path.join(self.temp_dir, "thumbnail_grid.jpg")
        
        cols, rows = grid_size
        thumb_width, thumb_height = thumbnail_size
        
        # Create blank canvas
        canvas_width = cols * thumb_width
        canvas_height = rows * thumb_height
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
        
        # Place thumbnails
        for i, image_path in enumerate(image_paths[:cols * rows]):
            if not os.path.exists(image_path):
                continue
                
            row = i // cols
            col = i % cols
            
            try:
                with Image.open(image_path) as img:
                    # Create thumbnail
                    img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                    
                    # Center the thumbnail in the allocated space
                    x = col * thumb_width + (thumb_width - img.width) // 2
                    y = row * thumb_height + (thumb_height - img.height) // 2
                    
                    canvas.paste(img, (x, y))
                    
            except Exception as e:
                self.logger.warning(f"Failed to process {image_path}: {e}")
                continue
        
        canvas.save(output_path)
        return output_path
    
    def optimize_for_pdf(self, image_path: str, max_width: int = 2000,
                        max_height: int = 2000, quality: int = 85,
                        output_path: Optional[str] = None) -> str:
        """
        Optimize image for PDF inclusion (resize and compress).
        
        Args:
            image_path: Path to input image
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            quality: JPEG quality (1-100)
            output_path: Path to save optimized image
            
        Returns:
            str: Path to optimized image
        """
        if output_path is None:
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_optimized.jpg"
        
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, 'white')
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if 'transparency' in img.info:
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if too large
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Save with compression
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            return output_path
    
    def batch_process_folder(self, input_folder: str, output_folder: str,
                           operations: List[str] = None) -> List[str]:
        """
        Batch process all images in a folder.
        
        Args:
            input_folder: Path to input folder
            output_folder: Path to output folder
            operations: List of operations to perform
            
        Returns:
            List[str]: Paths to processed images
        """
        if operations is None:
            operations = ['auto_rotate', 'optimize_for_pdf']
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        processed_files = []
        
        # Supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
        
        for filename in os.listdir(input_folder):
            if os.path.splitext(filename.lower())[1] not in image_extensions:
                continue
                
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            current_path = input_path
            
            try:
                # Apply operations in sequence
                for operation in operations:
                    if operation == 'auto_rotate':
                        current_path = self.auto_rotate_image(current_path, output_path)
                    elif operation == 'optimize_for_pdf':
                        current_path = self.optimize_for_pdf(current_path, output_path=output_path)
                    elif operation == 'enhance':
                        current_path = self.enhance_image(current_path, output_path=output_path)
                
                processed_files.append(current_path)
                self.logger.info(f"Processed: {filename}")
                
            except Exception as e:
                self.logger.error(f"Failed to process {filename}: {e}")
                continue
        
        return processed_files
