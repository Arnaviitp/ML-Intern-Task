"""
AI-Powered Image Generator
A text-to-image generation system using Stable Diffusion
"""

import streamlit as st
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import os
from datetime import datetime
import json
import io
from pathlib import Path
import gc

# Import custom modules
from utils.image_processor import ImageProcessor
from utils.prompt_engineer import PromptEngineer
from utils.config import Config
from utils.content_filter import ContentFilter

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Main container styling - Dark Mode */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Headings */
    h1 {
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        text-align: center;
        padding: 1.5rem 0;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
        background: linear-gradient(90deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h2, h3 {
        color: #e2e8f0;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1c24;
        border-right: 1px solid #2d3748;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(99, 102, 241, 0.4);
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* Input fields and select boxes */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #262730;
        border-radius: 8px;
        border: 1px solid #4b5563;
        color: #ffffff;
    }
    
    /* Text areas */
    .stTextArea>div>div>textarea {
        background-color: #262730;
        border-radius: 8px;
        border: 1px solid #4b5563;
        color: #ffffff;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #262730;
        border-radius: 8px;
        border: 1px solid #4b5563;
        color: #ffffff;
    }
    
    /* Custom info box */
    .info-box {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #6366f1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
        color: #e2e8f0;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        padding: 1rem;
        border-radius: 8px;
        background-color: #1e293b;
        color: #ffffff;
    }
    
    /* Labels */
    .stMarkdown p, label {
        color: #e2e8f0 !important;
    }
    </style>
""", unsafe_allow_html=True)


class ImageGenerator:
    """Main class for AI Image Generation"""
    
    def __init__(self):
        self.config = Config()
        self.filter = ContentFilter()
        self.prompt_engineer = PromptEngineer()
        self.image_processor = ImageProcessor()
        self.pipeline = None
        self.device = self._detect_device()
        
    def _detect_device(self):
        """Detect and return the best available device"""
        if torch.cuda.is_available():
            device = "cuda"
            st.sidebar.success(f"✅ GPU Detected: {torch.cuda.get_device_name(0)}")
        else:
            device = "cpu"
            st.sidebar.warning("⚠️ Running on CPU (slower generation)")
        return device
    
    @st.cache_resource
    def load_model(_self, model_name):
        """Load the Stable Diffusion model"""
        try:
            with st.spinner(f"Loading {model_name}... This may take a few minutes on first run."):
                # Load pipeline
                pipe = StableDiffusionPipeline.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if _self.device == "cuda" else torch.float32,
                    safety_checker=None,  # We'll use our custom filter
                    requires_safety_checker=False
                )
                
                # Optimize scheduler for faster generation
                pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                    pipe.scheduler.config
                )
                
                # Move to device
                pipe = pipe.to(_self.device)
                
                # Enable memory optimizations
                if _self.device == "cuda":
                    pipe.enable_attention_slicing()
                    pipe.enable_vae_slicing()
                
                st.success("✅ Model loaded successfully!")
                return pipe
                
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            st.info("💡 Tip: Run `python utils/model_downloader.py` to download the model first")
            return None
    
    def generate_images(self, prompt, negative_prompt, num_images, 
                       guidance_scale, num_inference_steps, seed, 
                       width, height, enhance_prompt):
        """Generate images based on parameters"""
        
        # Content filtering
        if not self.filter.is_safe(prompt):
            st.error("⛔ This prompt contains inappropriate content and cannot be processed.")
            st.info("Please modify your prompt to comply with ethical AI guidelines.")
            return []
        
        # Prompt engineering
        if enhance_prompt:
            enhanced_prompt = self.prompt_engineer.enhance_prompt(prompt)
            st.info(f"📝 Enhanced prompt: {enhanced_prompt}")
            prompt = enhanced_prompt
        
        # Set seed for reproducibility
        generator = torch.Generator(device=self.device)
        if seed > 0:
            generator = generator.manual_seed(seed)
        
        images = []
        metadata_list = []
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(num_images):
            status_text.text(f"Generating image {i+1}/{num_images}...")
            progress_bar.progress((i) / num_images)
            
            try:
                # Generate image
                # with torch.autocast(self.device): # Removed for CPU stability
                output = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height,
                    generator=generator
                )
                
                image = output.images[0]
                
                # Add watermark
                image = self.image_processor.add_watermark(image)
                
                # Store metadata
                metadata = {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "model": self.config.DEFAULT_MODEL,
                    "parameters": {
                        "guidance_scale": guidance_scale,
                        "num_inference_steps": num_inference_steps,
                        "seed": seed if seed > 0 else "random",
                        "width": width,
                        "height": height
                    }
                }
                
                images.append(image)
                metadata_list.append(metadata)
                
                # Clear cache
                if self.device == "cuda":
                    torch.cuda.empty_cache()
                gc.collect()
                
            except Exception as e:
                st.error(f"Error generating image {i+1}: {str(e)}")
        
        progress_bar.progress(1.0)
        status_text.text("✅ Generation complete!")
        
        return list(zip(images, metadata_list))
    
    def save_images(self, image_metadata_pairs, format_type):
        """Save generated images with metadata"""
        saved_files = []
        
        for idx, (image, metadata) in enumerate(image_metadata_pairs):
            # Create output directory
            output_dir = Path(self.config.OUTPUT_DIR)
            output_dir.mkdir(exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}_{idx+1}.{format_type.lower()}"
            filepath = output_dir / filename
            
            # Save image
            image.save(filepath, format=format_type)
            
            # Save metadata
            metadata_path = output_dir / f"metadata_{timestamp}_{idx+1}.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            saved_files.append(str(filepath))
        
        return saved_files


def main():
    """Main application"""
    
    # Header
    st.markdown("<h1>🎨 AI-Powered Image Generator</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize generator
    if 'generator' not in st.session_state:
        st.session_state.generator = ImageGenerator()
    
    generator = st.session_state.generator
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        st.subheader("Model Settings")
        model_options = {
            "Stable Diffusion v1.5": "runwayml/stable-diffusion-v1-5",
            "Stable Diffusion v2.1": "stabilityai/stable-diffusion-2-1",
        }
        
        selected_model_name = st.selectbox(
            "Select Model",
            list(model_options.keys()),
            help="Choose the AI model for image generation"
        )
        
        selected_model = model_options[selected_model_name]
        
        # Load model button
        if st.button("🔄 Load Model"):
            generator.pipeline = generator.load_model(selected_model)
        
        st.markdown("---")
        
        # Generation parameters
        st.subheader("Generation Parameters")
        
        num_images = st.slider(
            "Number of Images",
            min_value=1,
            max_value=4,
            value=1,
            help="Number of images to generate per prompt"
        )
        
        guidance_scale = st.slider(
            "Guidance Scale",
            min_value=1.0,
            max_value=20.0,
            value=7.5,
            step=0.5,
            help="Higher values = more adherence to prompt (7-12 recommended)"
        )
        
        # Determine default steps based on device
        default_steps = 50 if generator.device == "cuda" else 20
        
        num_inference_steps = st.slider(
            "Inference Steps",
            min_value=10,
            max_value=100,
            value=default_steps,
            step=5,
            help="More steps = better quality but slower (30-50 recommended)"
        )
        
        if generator.device == "cpu":
             st.caption("⚠️ CPU detected: Lower steps (20-25) recommended for faster generation.")
        
        seed = st.number_input(
            "Seed (0 for random)",
            min_value=0,
            max_value=2147483647,
            value=0,
            help="Use same seed for reproducible results"
        )
        
        st.markdown("---")
        
        # Image dimensions
        st.subheader("Image Dimensions")
        
        width = st.selectbox(
            "Width",
            [512, 768, 1024],
            index=0,
            help="Image width in pixels"
        )
        
        height = st.selectbox(
            "Height",
            [512, 768, 1024],
            index=0,
            help="Image height in pixels"
        )
        
        st.markdown("---")
        
        # Export settings
        st.subheader("Export Settings")
        format_type = st.selectbox(
            "Image Format",
            ["PNG", "JPEG"],
            help="Output image format"
        )
        
        st.markdown("---")
        
        # System info
        st.subheader("System Information")
        st.info(f"""
        **Device:** {generator.device.upper()}
        **PyTorch:** {torch.__version__}
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Prompt Configuration")
        
        # Main prompt
        prompt = st.text_area(
            "Enter your prompt",
            height=100,
            placeholder="Example: A beautiful sunset over mountains, highly detailed, 8k, photorealistic",
            help="Describe what you want to generate"
        )
        
        # Prompt enhancement
        enhance_prompt = st.checkbox(
            "Enhance prompt automatically",
            value=True,
            help="Add quality-improving descriptors to your prompt"
        )
        
        # Negative prompt
        use_negative = st.checkbox("Use negative prompt", value=True)
        
        if use_negative:
            negative_prompt = st.text_area(
                "Negative prompt (what to avoid)",
                height=80,
                value="blurry, low quality, distorted, deformed, ugly, bad anatomy",
                help="Describe what you DON'T want in the image"
            )
        else:
            negative_prompt = ""
        
        # Style presets
        st.subheader("🎨 Style Presets")
        style_preset = st.selectbox(
            "Choose a style",
            [
                "None",
                "Photorealistic",
                "Digital Art",
                "Oil Painting",
                "Watercolor",
                "Anime/Manga",
                "3D Render",
                "Pencil Sketch",
                "Cyberpunk",
                "Fantasy Art"
            ]
        )
        
        if style_preset != "None":
            style_suffix = PromptEngineer.get_style_suffix(style_preset)
            st.info(f"Style addition: {style_suffix}")
            if prompt and style_suffix:
                prompt = f"{prompt}, {style_suffix}"
        
        # Generate button
        st.markdown("---")
        generate_button = st.button("🚀 Generate Images", type="primary")
    
    with col2:
        st.subheader("🖼️ Generated Images")
        
        if generate_button:
            if not generator.pipeline:
                st.error("⚠️ Please load a model first using the sidebar!")
            elif not prompt:
                st.warning("⚠️ Please enter a prompt!")
            else:
                # Generate images
                results = generator.generate_images(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_images=num_images,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    seed=seed,
                    width=width,
                    height=height,
                    enhance_prompt=enhance_prompt
                )
                
                if results:
                    # Store in session state
                    st.session_state.last_results = results
                    st.session_state.last_format = format_type
        
        # Display results
        if 'last_results' in st.session_state:
            results = st.session_state.last_results
            
            for idx, (image, metadata) in enumerate(results):
                st.image(image, caption=f"Image {idx+1}", use_container_width=True)
                
                # Download button
                buf = io.BytesIO()
                image.save(buf, format=st.session_state.last_format)
                btn = st.download_button(
                    label=f"⬇️ Download Image {idx+1}",
                    data=buf.getvalue(),
                    file_name=f"generated_{idx+1}.{st.session_state.last_format.lower()}",
                    mime=f"image/{st.session_state.last_format.lower()}"
                )
                
                # Show metadata
                with st.expander(f"📊 Metadata for Image {idx+1}"):
                    st.json(metadata)
            
            # Save all button
            if st.button("💾 Save All Images"):
                saved_files = generator.save_images(results, st.session_state.last_format)
                st.success(f"✅ Saved {len(saved_files)} images to {generator.config.OUTPUT_DIR}")
                for file in saved_files:
                    st.text(f"• {file}")
    
    # Information section
    st.markdown("---")
    st.markdown("### 💡 Prompt Engineering Tips")
    
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.markdown("""
        **Quality Boosters:**
        - "highly detailed"
        - "8k resolution"
        - "professional"
        - "masterpiece"
        """)
    
    with tips_col2:
        st.markdown("""
        **Style Keywords:**
        - "photorealistic"
        - "digital art"
        - "oil painting"
        - "cinematic lighting"
        """)
    
    with tips_col3:
        st.markdown("""
        **Camera/Composition:**
        - "close-up portrait"
        - "wide angle shot"
        - "bokeh background"
        - "golden hour lighting"
        """)
    
    # Ethical guidelines
    with st.expander("⚖️ Ethical AI Guidelines"):
        st.markdown("""
        ### Responsible Use Guidelines
        
        **DO:**
        - Create original artwork and creative content
        - Use for learning and experimentation
        - Give credit when sharing AI-generated images
        - Respect intellectual property rights
        
        **DON'T:**
        - Generate content depicting real people without consent
        - Create misleading or deceptive content
        - Generate illegal, harmful, or inappropriate content
        - Use for commercial purposes without proper rights
        
        **Note:** All generated images are watermarked to indicate AI origin.
        """)


if __name__ == "__main__":
    main()
