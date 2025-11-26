"""
Image processing utilities for the AI Image Generator
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
from pathlib import Path
from utils.config import Config


class ImageProcessor:
    """Class for image processing operations"""
    
    def __init__(self):
        self.config = Config()
    
    def add_watermark(self, image: Image.Image, 
                     text: str = None, 
                     position: str = "bottom-right") -> Image.Image:
        """
        Add watermark to an image
        
        Args:
            image (PIL.Image): Original image
            text (str): Watermark text (default from config)
            position (str): Position of watermark
            
        Returns:
            PIL.Image: Watermarked image
        """
        if text is None:
            text = self.config.WATERMARK_TEXT
        
        # Create a copy to avoid modifying original
        watermarked = image.copy()
        
        # Create drawing context
        draw = ImageDraw.Draw(watermarked)
        
        # Calculate text size and position
        try:
            # Try to use a nice font
            font = ImageFont.truetype("arial.ttf", self.config.WATERMARK_FONT_SIZE)
        except:
            # Fall back to default font
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        margin = 10
        if position == "bottom-right":
            x = watermarked.width - text_width - margin
            y = watermarked.height - text_height - margin
        elif position == "bottom-left":
            x = margin
            y = watermarked.height - text_height - margin
        elif position == "top-right":
            x = watermarked.width - text_width - margin
            y = margin
        elif position == "top-left":
            x = margin
            y = margin
        else:  # center
            x = (watermarked.width - text_width) // 2
            y = (watermarked.height - text_height) // 2
        
        # Create semi-transparent overlay
        overlay = Image.new('RGBA', watermarked.size, (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Draw text with opacity
        overlay_draw.text(
            (x, y), 
            text, 
            font=font, 
            fill=(255, 255, 255, self.config.WATERMARK_OPACITY)
        )
        
        # Convert original to RGBA if needed
        if watermarked.mode != 'RGBA':
            watermarked = watermarked.convert('RGBA')
        
        # Composite the overlay
        watermarked = Image.alpha_composite(watermarked, overlay)
        
        # Convert back to RGB
        if watermarked.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', watermarked.size, (255, 255, 255))
            background.paste(watermarked, mask=watermarked.split()[3])
            watermarked = background
        
        return watermarked
    
    def resize_image(self, image: Image.Image, 
                    width: int = None, 
                    height: int = None,
                    maintain_aspect: bool = True) -> Image.Image:
        """
        Resize an image
        
        Args:
            image (PIL.Image): Original image
            width (int): Target width
            height (int): Target height
            maintain_aspect (bool): Maintain aspect ratio
            
        Returns:
            PIL.Image: Resized image
        """
        if width is None and height is None:
            return image
        
        original_width, original_height = image.size
        
        if maintain_aspect:
            if width and height:
                # Calculate aspect ratios
                aspect_ratio = original_width / original_height
                target_aspect = width / height
                
                if aspect_ratio > target_aspect:
                    # Width is limiting factor
                    new_width = width
                    new_height = int(width / aspect_ratio)
                else:
                    # Height is limiting factor
                    new_height = height
                    new_width = int(height * aspect_ratio)
            elif width:
                aspect_ratio = original_width / original_height
                new_width = width
                new_height = int(width / aspect_ratio)
            else:  # height only
                aspect_ratio = original_width / original_height
                new_height = height
                new_width = int(height * aspect_ratio)
        else:
            new_width = width or original_width
            new_height = height or original_height
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def enhance_image(self, image: Image.Image,
                     brightness: float = 1.0,
                     contrast: float = 1.0,
                     sharpness: float = 1.0,
                     saturation: float = 1.0) -> Image.Image:
        """
        Enhance image with various parameters
        
        Args:
            image (PIL.Image): Original image
            brightness (float): Brightness factor (1.0 = original)
            contrast (float): Contrast factor (1.0 = original)
            sharpness (float): Sharpness factor (1.0 = original)
            saturation (float): Color saturation (1.0 = original)
            
        Returns:
            PIL.Image: Enhanced image
        """
        enhanced = image.copy()
        
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(enhanced)
            enhanced = enhancer.enhance(brightness)
        
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(enhanced)
            enhanced = enhancer.enhance(contrast)
        
        if sharpness != 1.0:
            enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = enhancer.enhance(sharpness)
        
        if saturation != 1.0:
            enhancer = ImageEnhance.Color(enhanced)
            enhanced = enhancer.enhance(saturation)
        
        return enhanced
    
    def convert_format(self, image: Image.Image, format_type: str) -> bytes:
        """
        Convert image to specified format
        
        Args:
            image (PIL.Image): Image to convert
            format_type (str): Target format (PNG, JPEG, WEBP)
            
        Returns:
            bytes: Image data in specified format
        """
        buffer = io.BytesIO()
        
        # Handle RGBA for JPEG
        if format_type.upper() == "JPEG" and image.mode == "RGBA":
            # Create white background
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3] if len(image.split()) == 4 else None)
            image = background
        
        image.save(buffer, format=format_type.upper())
        return buffer.getvalue()
    
    def create_thumbnail(self, image: Image.Image, size: tuple = (256, 256)) -> Image.Image:
        """
        Create a thumbnail of the image
        
        Args:
            image (PIL.Image): Original image
            size (tuple): Thumbnail size (width, height)
            
        Returns:
            PIL.Image: Thumbnail image
        """
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail
    
    def apply_filter(self, image: Image.Image, filter_name: str) -> Image.Image:
        """
        Apply predefined filters to image
        
        Args:
            image (PIL.Image): Original image
            filter_name (str): Filter name
            
        Returns:
            PIL.Image: Filtered image
        """
        if filter_name == "vintage":
            return self.enhance_image(
                image,
                brightness=0.9,
                contrast=1.2,
                saturation=0.7
            )
        elif filter_name == "vibrant":
            return self.enhance_image(
                image,
                brightness=1.1,
                contrast=1.3,
                saturation=1.4,
                sharpness=1.2
            )
        elif filter_name == "soft":
            return self.enhance_image(
                image,
                brightness=1.1,
                contrast=0.9,
                sharpness=0.8
            )
        elif filter_name == "dramatic":
            return self.enhance_image(
                image,
                brightness=0.9,
                contrast=1.5,
                saturation=1.2,
                sharpness=1.3
            )
        else:
            return image
