"""
Configuration settings for AI Image Generator
"""

class Config:
    """Configuration class for the application"""
    
    # Model settings
    DEFAULT_MODEL = "runwayml/stable-diffusion-v1-5"
    
    # Generation defaults
    DEFAULT_WIDTH = 512
    DEFAULT_HEIGHT = 512
    DEFAULT_GUIDANCE_SCALE = 7.5
    DEFAULT_INFERENCE_STEPS = 50
    DEFAULT_NUM_IMAGES = 1
    
    # Output settings
    OUTPUT_DIR = "generated_images"
    DEFAULT_FORMAT = "PNG"
    
    # Watermark settings
    WATERMARK_TEXT = "AI Generated"
    WATERMARK_OPACITY = 128
    WATERMARK_FONT_SIZE = 20
    
    # Content filtering
    ENABLE_CONTENT_FILTER = True
    
    # Memory optimization
    ENABLE_ATTENTION_SLICING = True
    ENABLE_VAE_SLICING = True
    
    # Supported image formats
    SUPPORTED_FORMATS = ["PNG", "JPEG", "WEBP"]
    
    # Style presets
    STYLE_PRESETS = {
        "Photorealistic": "highly detailed, professional photography, 8k, photorealistic",
        "Digital Art": "digital art, trending on artstation, highly detailed",
        "Oil Painting": "oil painting, classical art style, detailed brushwork",
        "Watercolor": "watercolor painting, soft colors, artistic",
        "Anime/Manga": "anime style, manga art, vibrant colors",
        "3D Render": "3d render, octane render, unreal engine, highly detailed",
        "Pencil Sketch": "pencil sketch, graphite drawing, detailed linework",
        "Cyberpunk": "cyberpunk, neon lights, futuristic, dystopian",
        "Fantasy Art": "fantasy art, magical, ethereal, highly detailed"
    }
    
    # Quality enhancers
    QUALITY_ENHANCERS = [
        "highly detailed",
        "ultra detailed",
        "8k resolution",
        "professional",
        "high quality",
        "masterpiece",
        "best quality"
    ]
    
    # Common negative prompts
    DEFAULT_NEGATIVE_PROMPTS = [
        "blurry",
        "low quality",
        "low resolution",
        "distorted",
        "deformed",
        "ugly",
        "bad anatomy",
        "bad proportions",
        "watermark",
        "signature",
        "text"
    ]
