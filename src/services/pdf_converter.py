"""
PDF conversion services for the Image-to-PDF Organizer.

This module handles the conversion of images to PDF files with
various options for page size, compression, and layout.
"""

import os
import img2pdf
from PIL import Image
from typing import List, Tuple, Literal, Optional
import tempfile
import shutil


class PDFConverter:
    """Class for converting images to PDF."""

    # Standard page sizes in points (1 point = 1/72 inch)
    PAGE_SIZES = {
        'A4': (595, 842),       # 210 x 297 mm
        'LETTER': (612, 792),   # 8.5 x 11 inches
        'LEGAL': (612, 1008),   # 8.5 x 14 inches
        'TABLOID': (792, 1224)  # 11 x 17 inches
    }
    
    def __init__(self):
        """Initialize the PDF converter."""
        self.temp_dir = tempfile.mkdtemp()
    
    def __del__(self):
        """Clean up temporary files."""
        try:
            shutil.rmtree(self.temp_dir)
        except (OSError, AttributeError):
            pass
    
    def _prepare_images(self, image_paths: List[str], 
                       page_size: str, 
                       compress: bool = False,
                       compression_quality: int = 85) -> List[str]:
        """
        Prepare images for PDF conversion.
        
        Args:
            image_paths: List of paths to images
            page_size: Target page size ('A4', 'LETTER', etc., or 'FIT' for original size)
            compress: Whether to compress images
            compression_quality: Image quality for compression (1-100)
            
        Returns:
            List[str]: List of paths to prepared images
        """
        prepared_paths = []
        
        for i, img_path in enumerate(image_paths):
            # Create a copy of the image in the temp directory
            file_ext = os.path.splitext(img_path)[1]
            temp_path = os.path.join(self.temp_dir, f"image_{i}{file_ext}")
            
            with Image.open(img_path) as img:
                # Convert to RGB if necessary (PDF doesn't support RGBA)
                if img.mode == 'RGBA':
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3])
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if a specific page size is requested
                if page_size != 'FIT' and page_size in self.PAGE_SIZES:
                    pdf_width, pdf_height = self.PAGE_SIZES[page_size]
                    img_width, img_height = img.size
                    
                    # Calculate aspect ratios
                    page_ratio = pdf_width / pdf_height
                    img_ratio = img_width / img_height
                    
                    # Resize to fit within page while maintaining aspect ratio
                    if img_ratio > page_ratio:  # Image is wider
                        new_width = pdf_width
                        new_height = int(pdf_width / img_ratio)
                    else:  # Image is taller
                        new_height = pdf_height
                        new_width = int(pdf_height * img_ratio)
                    
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Compress if requested
                if compress:
                    img.save(temp_path, quality=compression_quality, optimize=True)
                else:
                    img.save(temp_path)
            
            prepared_paths.append(temp_path)
        
        return prepared_paths
    
    def convert_images_to_pdf(self, 
                             image_paths: List[str], 
                             output_path: str, 
                             page_size: Literal['A4', 'LETTER', 'LEGAL', 'TABLOID', 'FIT'] = 'A4',
                             compress: bool = False,
                             compression_quality: int = 85,
                             callback=None) -> str:
        """
        Convert a list of images to a single PDF file.
        
        Args:
            image_paths: List of paths to images
            output_path: Path where the PDF will be saved
            page_size: Target page size or 'FIT' to use original image dimensions
            compress: Whether to compress images before conversion
            compression_quality: Image quality for compression (1-100)
            callback: Optional callback function to report progress (receives a float 0-1)
            
        Returns:
            str: Path to the created PDF file
        """
        if not image_paths:
            raise ValueError("No images provided for conversion")
        
        total_images = len(image_paths)
        prepared_paths = self._prepare_images(
            image_paths, page_size, compress, compression_quality
        )
        
        # Convert images to PDF with basic functionality
        try:
            if page_size != 'FIT' and page_size in self.PAGE_SIZES:
                # Use specified page size
                page_width, page_height = self.PAGE_SIZES[page_size]
                # Convert points to mm for img2pdf
                page_width_mm = page_width * 0.352778
                page_height_mm = page_height * 0.352778
                
                # Create PDF with specified page size
                with open(output_path, "wb") as f:
                    f.write(img2pdf.convert(prepared_paths, 
                                          layout_fun=img2pdf.get_layout_fun(
                                              pagesize=(page_width_mm, page_height_mm)
                                          )))
            else:
                # Use original image dimensions (FIT mode)
                with open(output_path, "wb") as f:
                    f.write(img2pdf.convert(prepared_paths))
            
            # Report progress if callback is provided
            if callback:
                callback(1.0)  # 100% complete
                
        except Exception as e:
            raise Exception(f"Failed to convert images to PDF: {str(e)}")
        
        return output_path
