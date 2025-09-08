"""
Image Effects Plugin - Advanced image effects and filters.
"""

import os
import tempfile
from typing import Dict, Any
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

# Import plugin interface from parent directory
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from plugin_system import ImageProcessorPlugin


class ImageEffectsPlugin(ImageProcessorPlugin):
    """Plugin for applying various image effects."""
    
    @property
    def name(self) -> str:
        return "Image Effects"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Advanced image effects and filters including blur, sharpen, vintage, sepia, and more"
    
    @property
    def author(self) -> str:
        return "PDF Organizer Team"
    
    def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            # Verify dependencies
            import numpy
            from PIL import Image, ImageFilter, ImageEnhance
            print(f"Initialized {self.name} plugin")
            return True
        except ImportError as e:
            print(f"Missing dependency for {self.name}: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Cleanup when plugin is unloaded."""
        print(f"Cleaned up {self.name} plugin")
        return True
    
    def process_image(self, image_path: str, **kwargs) -> str:
        """
        Apply effects to an image.
        
        Args:
            image_path: Path to the input image
            **kwargs: Effect parameters
            
        Returns:
            str: Path to the processed image
        """
        effect = kwargs.get('effect', 'none')
        intensity = kwargs.get('intensity', 1.0)
        
        # Open image
        image = Image.open(image_path)
        
        # Apply the selected effect
        if effect == 'blur':
            processed = self._apply_blur(image, intensity)
        elif effect == 'sharpen':
            processed = self._apply_sharpen(image, intensity)
        elif effect == 'vintage':
            processed = self._apply_vintage(image, intensity)
        elif effect == 'sepia':
            processed = self._apply_sepia(image, intensity)
        elif effect == 'black_white':
            processed = self._apply_black_white(image)
        elif effect == 'enhance_colors':
            processed = self._apply_color_enhancement(image, intensity)
        elif effect == 'edge_enhance':
            processed = self._apply_edge_enhancement(image, intensity)
        elif effect == 'emboss':
            processed = self._apply_emboss(image)
        elif effect == 'oil_painting':
            processed = self._apply_oil_painting(image)
        else:
            processed = image  # No effect
        
        # Save processed image
        temp_dir = tempfile.gettempdir()
        filename = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(temp_dir, f"{filename}_{effect}_processed.png")
        
        processed.save(output_path, "PNG")
        return output_path
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get plugin parameters schema."""
        return {
            'effect': {
                'type': 'select',
                'options': [
                    'none', 'blur', 'sharpen', 'vintage', 'sepia',
                    'black_white', 'enhance_colors', 'edge_enhance',
                    'emboss', 'oil_painting'
                ],
                'default': 'none',
                'description': 'Image effect to apply'
            },
            'intensity': {
                'type': 'slider',
                'min': 0.1,
                'max': 3.0,
                'step': 0.1,
                'default': 1.0,
                'description': 'Effect intensity'
            }
        }
    
    def _apply_blur(self, image: Image.Image, intensity: float) -> Image.Image:
        """Apply blur effect."""
        radius = min(10, max(0.1, intensity * 2))
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    def _apply_sharpen(self, image: Image.Image, intensity: float) -> Image.Image:
        """Apply sharpen effect."""
        enhancer = ImageEnhance.Sharpness(image)
        factor = 1.0 + intensity
        return enhancer.enhance(factor)
    
    def _apply_vintage(self, image: Image.Image, intensity: float) -> Image.Image:
        """Apply vintage effect."""
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply sepia tone
        sepia_image = self._apply_sepia(image, intensity * 0.7)
        
        # Reduce contrast slightly
        contrast_enhancer = ImageEnhance.Contrast(sepia_image)
        vintage_image = contrast_enhancer.enhance(0.9)
        
        # Add slight blur for aged effect
        vintage_image = vintage_image.filter(ImageFilter.GaussianBlur(radius=0.3))
        
        return vintage_image
    
    def _apply_sepia(self, image: Image.Image, intensity: float) -> Image.Image:
        """Apply sepia effect."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        pixels = np.array(image)
        
        # Sepia transformation matrix
        sepia_filter = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        
        # Apply sepia transformation
        sepia_img = pixels @ sepia_filter.T
        
        # Ensure values are in valid range
        sepia_img = np.clip(sepia_img, 0, 255)
        
        # Blend with original based on intensity
        if intensity < 1.0:
            sepia_img = pixels * (1 - intensity) + sepia_img * intensity
        
        return Image.fromarray(sepia_img.astype(np.uint8))
    
    def _apply_black_white(self, image: Image.Image) -> Image.Image:
        """Apply black and white effect."""
        return image.convert('L').convert('RGB')
    
    def _apply_color_enhancement(self, image: Image.Image, intensity: float) -> Image.Image:
        """Apply color enhancement."""
        enhancer = ImageEnhance.Color(image)
        factor = 1.0 + (intensity - 1.0) * 0.5
        return enhancer.enhance(factor)
    
    def _apply_edge_enhancement(self, image: Image.Image, intensity: float) -> Image.Image:
        """Apply edge enhancement."""
        edge_filter = ImageFilter.EDGE_ENHANCE_MORE if intensity > 1.5 else ImageFilter.EDGE_ENHANCE
        enhanced = image.filter(edge_filter)
        
        # Blend with original based on intensity
        from PIL import Image as PILImage
        return PILImage.blend(image, enhanced, min(1.0, intensity * 0.3))
    
    def _apply_emboss(self, image: Image.Image) -> Image.Image:
        """Apply emboss effect."""
        return image.filter(ImageFilter.EMBOSS)
    
    def _apply_oil_painting(self, image: Image.Image) -> Image.Image:
        """Apply oil painting effect."""
        # Simple oil painting approximation using median filter
        oil_image = image.filter(ImageFilter.MedianFilter(size=3))
        
        # Apply slight blur
        oil_image = oil_image.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Enhance colors slightly
        enhancer = ImageEnhance.Color(oil_image)
        oil_image = enhancer.enhance(1.2)
        
        return oil_image


# Plugin factory function (optional)
def create_plugin():
    """Factory function to create plugin instance."""
    return ImageEffectsPlugin()
