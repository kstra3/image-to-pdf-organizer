"""
Tests for the image handler service.
"""

import os
import tempfile
import pytest
from PIL import Image
from src.services.image_handler import ImageHandler


@pytest.fixture
def temp_image():
    """Create a temporary test image and return its path."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test image
        img_path = os.path.join(temp_dir, "test_image.jpg")
        img = Image.new('RGB', (100, 100), color='red')
        img.save(img_path)
        
        yield img_path


def test_is_valid_image():
    """Test the is_valid_image method."""
    # Test valid extensions
    assert ImageHandler.is_valid_image("test.jpg") is True
    assert ImageHandler.is_valid_image("test.jpeg") is True
    assert ImageHandler.is_valid_image("test.png") is True
    assert ImageHandler.is_valid_image("test.bmp") is True
    assert ImageHandler.is_valid_image("test.tiff") is True
    assert ImageHandler.is_valid_image("test.gif") is True
    
    # Test invalid extensions
    assert ImageHandler.is_valid_image("test.pdf") is False
    assert ImageHandler.is_valid_image("test.txt") is False
    assert ImageHandler.is_valid_image("test") is False


def test_get_image_dimensions(temp_image):
    """Test the get_image_dimensions method."""
    # Get dimensions of the test image
    width, height = ImageHandler.get_image_dimensions(temp_image)
    
    # The test image is 100x100
    assert width == 100
    assert height == 100


def test_resize_image(temp_image):
    """Test the resize_image method."""
    # Create a new path for the resized image
    temp_dir = os.path.dirname(temp_image)
    resized_path = os.path.join(temp_dir, "resized.jpg")
    
    # Resize the image to 50x50
    ImageHandler.resize_image(temp_image, (50, 50), resized_path)
    
    # Check if the resized image exists
    assert os.path.exists(resized_path)
    
    # Check the dimensions of the resized image
    with Image.open(resized_path) as img:
        assert img.size == (50, 50)


def test_compress_image(temp_image):
    """Test the compress_image method."""
    # Create a new path for the compressed image
    temp_dir = os.path.dirname(temp_image)
    compressed_path = os.path.join(temp_dir, "compressed.jpg")
    
    # Get the original file size
    original_size = os.path.getsize(temp_image)
    
    # Compress the image with low quality
    ImageHandler.compress_image(temp_image, quality=10, output_path=compressed_path)
    
    # Check if the compressed image exists
    assert os.path.exists(compressed_path)
    
    # Check if the file size has decreased
    compressed_size = os.path.getsize(compressed_path)
    assert compressed_size < original_size
