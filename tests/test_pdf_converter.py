"""
Tests for the PDF converter service.
"""

import os
import tempfile
import pytest
from PIL import Image
import img2pdf
from src.services.pdf_converter import PDFConverter


@pytest.fixture
def temp_images():
    """Create temporary test images and return their paths."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create multiple test images
        image_paths = []
        
        for i in range(3):
            img_path = os.path.join(temp_dir, f"test_image_{i}.jpg")
            img = Image.new('RGB', (100, 100), color=(255, 0, 0) if i == 0 else
                                                     (0, 255, 0) if i == 1 else
                                                     (0, 0, 255))
            img.save(img_path)
            image_paths.append(img_path)
        
        yield image_paths, temp_dir


def test_pdf_converter_init():
    """Test PDFConverter initialization."""
    converter = PDFConverter()
    assert converter.temp_dir is not None
    assert os.path.exists(converter.temp_dir)


def test_convert_images_to_pdf(temp_images):
    """Test the convert_images_to_pdf method."""
    image_paths, temp_dir = temp_images
    output_path = os.path.join(temp_dir, "output.pdf")
    
    # Test default parameters
    converter = PDFConverter()
    converter.convert_images_to_pdf(
        image_paths=image_paths,
        output_path=output_path
    )
    
    # Check if the PDF was created
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0


def test_convert_images_to_pdf_with_compression(temp_images):
    """Test PDF conversion with compression."""
    image_paths, temp_dir = temp_images
    output_path = os.path.join(temp_dir, "output_compressed.pdf")
    
    # Test with compression
    converter = PDFConverter()
    converter.convert_images_to_pdf(
        image_paths=image_paths,
        output_path=output_path,
        compress=True,
        compression_quality=50
    )
    
    # Check if the PDF was created
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0


def test_convert_images_to_pdf_with_different_page_sizes(temp_images):
    """Test PDF conversion with different page sizes."""
    image_paths, temp_dir = temp_images
    
    for page_size in ['A4', 'LETTER', 'LEGAL', 'TABLOID', 'FIT']:
        output_path = os.path.join(temp_dir, f"output_{page_size}.pdf")
        
        # Test with different page sizes
        converter = PDFConverter()
        converter.convert_images_to_pdf(
            image_paths=image_paths,
            output_path=output_path,
            page_size=page_size
        )
        
        # Check if the PDF was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0


def test_convert_images_to_pdf_with_callback(temp_images):
    """Test PDF conversion with progress callback."""
    image_paths, temp_dir = temp_images
    output_path = os.path.join(temp_dir, "output_callback.pdf")
    
    # Track progress updates
    progress_values = []
    
    def callback(progress):
        progress_values.append(progress)
    
    # Test with callback
    converter = PDFConverter()
    converter.convert_images_to_pdf(
        image_paths=image_paths,
        output_path=output_path,
        callback=callback
    )
    
    # Check if the PDF was created
    assert os.path.exists(output_path)
    
    # Check if the callback was called
    assert len(progress_values) > 0
    assert progress_values[-1] == 1.0  # Final progress should be 100%


def test_convert_empty_image_list():
    """Test handling of empty image list."""
    converter = PDFConverter()
    
    with pytest.raises(ValueError, match="No images provided for conversion"):
        converter.convert_images_to_pdf(
            image_paths=[],
            output_path="should_not_be_created.pdf"
        )
