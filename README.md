# 🎨 AI-Powered Image Generator

A comprehensive text-to-image generation system built with **Stable Diffusion**, featuring an intuitive web interface, advanced prompt engineering, and ethical AI safeguards.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Hardware Requirements](#hardware-requirements)
- [Usage](#usage)
- [Prompt Engineering Guide](#prompt-engineering-guide)
- [Technology Stack](#technology-stack)
- [Ethical Guidelines](#ethical-guidelines)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Troubleshooting](#troubleshooting)

## 🌟 Overview

This AI-Powered Image Generator transforms textual descriptions into high-quality images using open-source Stable Diffusion models. Built with a focus on accessibility, ethical AI use, and user experience, it provides both beginners and advanced users with powerful image generation capabilities.

### Key Highlights

- ✅ **100% Open Source** - No paid APIs or subscriptions
- 🚀 **GPU & CPU Support** - Runs on various hardware configurations
- 🎨 **Advanced Prompt Engineering** - Automatic prompt enhancement
- 🛡️ **Content Filtering** - Ethical AI safeguards built-in
- 💾 **Metadata Tracking** - Full generation history with parameters
- 🖼️ **Multiple Export Formats** - PNG, JPEG support
- ⚡ **Optimized Performance** - Memory-efficient processing

## ✨ Features

### Text-to-Image Generation
- Convert text prompts to stunning images
- Adjustable parameters (guidance scale, inference steps, seed)
- Multiple images per prompt (batch generation)
- Custom image dimensions (512×512, 768×768, 1024×1024)

### Style & Quality Control
- 9 built-in style presets (Photorealistic, Digital Art, Oil Painting, etc.)
- Automatic prompt enhancement with quality descriptors
- Negative prompts to filter unwanted elements
- Reproducible results with seed control

### User Interface
- Clean, modern Streamlit web interface
- Real-time generation progress tracking
- Image preview and download
- Metadata viewing for each generation
- Responsive design

### Ethical AI Features
- Content filtering for inappropriate prompts
- AI-generated watermarking
- Usage guidelines and best practices
- Privacy-conscious design

## 🏗️ Architecture

```
ML Task/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── prompt_engineer.py     # Prompt enhancement utilities
│   ├── content_filter.py      # Safety and content filtering
│   ├── image_processor.py     # Image processing utilities
│   └── model_downloader.py    # Model download utility
├── generated_images/           # Output directory (auto-created)
└── README.md                   # This file
```

### Component Overview

- **app.py**: Main application with UI and generation logic
- **prompt_engineer.py**: Enhances prompts for better results
- **content_filter.py**: Filters inappropriate content
- **image_processor.py**: Watermarking and image manipulation
- **model_downloader.py**: Downloads and manages AI models

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 10+ GB free disk space (for models)
- Git (optional, for cloning)

### Step-by-Step Guide

1. **Clone or download the repository**

```bash
cd "c:\Users\ML-Intern-Task"
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

**For GPU support (NVIDIA CUDA):**

```bash
# Install PyTorch with CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**For CPU-only:**

```bash
# The default requirements.txt includes CPU-compatible versions
pip install torch torchvision
```

4. **Download AI models**

```bash
python utils/model_downloader.py
```

This will download the Stable Diffusion model (~4-7 GB). You can choose:
- **Stable Diffusion v1.5** (Recommended, ~4 GB)
- **Stable Diffusion v2.1** (Advanced, ~5 GB)

## 💻 Hardware Requirements

### Minimum Requirements (CPU)
- **CPU**: Modern multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 16 GB
- **Storage**: 15 GB free space
- **Generation Time**: 3-10 minutes per image

### Recommended Requirements (GPU)
- **GPU**: NVIDIA GPU with 6+ GB VRAM (RTX 3060, RTX 3080, etc.)
- **CPU**: Intel i5/AMD Ryzen 5 or better
- **RAM**: 16 GB
- **Storage**: 15 GB free space
- **Generation Time**: 10-30 seconds per image

### Performance Comparison

| Hardware | Resolution | Steps | Time per Image |
|----------|-----------|-------|----------------|
| CPU (i7) | 512×512 | 50 | ~5 minutes |
| RTX 3060 | 512×512 | 50 | ~15 seconds |
| RTX 3080 | 512×512 | 50 | ~10 seconds |
| RTX 4090 | 1024×1024 | 50 | ~8 seconds |

## 🚀 Usage

### Starting the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Basic Workflow

1. **Load Model**
   - Click "Load Model" in the sidebar
   - Wait for model initialization (first time takes longer)

2. **Enter Prompt**
   - Type your description in the prompt box
   - Example: "A beautiful sunset over mountains, highly detailed, 8k"

3. **Adjust Settings** (optional)
   - Number of images: 1-4
   - Guidance scale: 7-12 (recommended)
   - Inference steps: 30-50 (recommended)
   - Image dimensions

4. **Generate**
   - Click "Generate Images"
   - Watch the progress bar
   - View and download results

### Example Prompts

**Portrait Photography:**
```
Professional portrait of a person, soft lighting, bokeh background, 
highly detailed, 8k, photorealistic
```

**Landscape:**
```
Beautiful mountain landscape at golden hour, dramatic clouds, 
professional photography, highly detailed
```

**Digital Art:**
```
Futuristic city with neon lights, cyberpunk style, rain-soaked streets, 
cinematic lighting, digital art, highly detailed
```

**Fantasy:**
```
Magical forest with glowing mushrooms, fantasy art style, 
ethereal lighting, mystical atmosphere, highly detailed
```

## 🎯 Prompt Engineering Guide

### Anatomy of a Good Prompt

A well-crafted prompt typically includes:

1. **Subject** - What you want to see
2. **Style** - Art style or medium
3. **Quality descriptors** - Detail level
4. **Lighting** - Lighting conditions
5. **Composition** - Camera angle or framing

**Example:**
```
[Subject: Dragon] in [Style: fantasy art style], [Quality: highly detailed, 8k], 
[Lighting: dramatic lighting], [Composition: epic perspective]
```

### Quality Boosters

Add these to improve image quality:
- "highly detailed"
- "8k resolution"
- "professional"
- "masterpiece"
- "ultra detailed"
- "sharp focus"

### Style Keywords

- **Photorealistic**: "photorealistic", "professional photography", "DSLR"
- **Digital Art**: "digital art", "trending on artstation"
- **Painting**: "oil painting", "watercolor", "acrylic"
- **3D**: "3d render", "octane render", "unreal engine"

### Lighting Terms

- "golden hour lighting"
- "soft lighting"
- "dramatic lighting"
- "cinematic lighting"
- "studio lighting"
- "natural lighting"

### Negative Prompts

Use negative prompts to avoid:
- "blurry"
- "low quality"
- "distorted"
- "deformed"
- "bad anatomy"
- "watermark"

### Tips & Best Practices

✅ **Do:**
- Be specific and descriptive
- Use quality enhancers
- Experiment with different styles
- Use negative prompts
- Keep prompts focused (10-40 words ideal)

❌ **Don't:**
- Use extremely long prompts (>50 words)
- Contradict yourself in the prompt
- Expect perfect results on first try
- Use copyrighted character names

## 🛠️ Technology Stack

### Core Technologies

- **Python 3.8+** - Programming language
- **PyTorch 2.0+** - Deep learning framework
- **Streamlit** - Web interface framework

### AI/ML Libraries

- **Diffusers (Hugging Face)** - Stable Diffusion implementation
- **Transformers** - Model management
- **Accelerate** - Performance optimization

### Image Processing

- **Pillow (PIL)** - Image manipulation
- **NumPy** - Numerical operations

### Models

- **Stable Diffusion v1.5** - Text-to-image model (default)
- **Stable Diffusion v2.1** - Advanced model (optional)

### Key Features of Stable Diffusion

- Open-source latent diffusion model
- 512×512 to 1024×1024 resolution support
- Fast inference with DPM-Solver scheduler
- Memory-efficient with attention slicing

## ⚖️ Ethical Guidelines

### Acceptable Use

✅ Creating original artistic works
✅ Generating illustrations for educational content
✅ Designing concepts and prototypes
✅ Personal creative projects
✅ Learning and experimentation

### Prohibited Use

❌ Generating images of real people without consent
❌ Creating misleading or deceptive content
❌ Producing illegal, harmful, or explicit content
❌ Infringing on copyrights or trademarks
❌ Generating content for harassment

### Best Practices

1. **Disclosure** - Always disclose that content is AI-generated
2. **Attribution** - Give credit when sharing
3. **Watermarking** - Use watermarks to indicate AI origin (built-in)
4. **Respect** - Respect intellectual property and privacy rights
5. **Responsibility** - Consider the impact of generated content

### Content Filtering

The application includes:
- Automatic blocking of inappropriate prompts
- Watermarking of all generated images
- Usage guidelines and warnings
- Sensitive content detection

## ⚠️ Limitations

### Technical Limitations

- **Generation Time**: CPU generation is significantly slower than GPU
- **Memory Requirements**: Large batches require more RAM/VRAM
- **Resolution**: Higher resolutions require more memory and time
- **Model Bias**: AI models may have inherent biases from training data

### Quality Limitations

- May struggle with:
  - Very specific details (e.g., exact text, precise counts)
  - Complex scenes with many objects
  - Photorealistic hands and faces (sometimes)
  - Rare or abstract concepts

### Best Results Tips

- Start with 512×512 resolution
- Use 30-50 inference steps
- Guidance scale between 7-12
- Be specific but not overly complex
- Iterate and refine prompts

## 🚧 Future Improvements

### Planned Features

1. **Model Fine-tuning**
   - Custom dataset training
   - Style-specific models
   - LoRA support

2. **Advanced Features**
   - Image-to-image generation
   - Inpainting (edit parts of images)
   - Outpainting (extend images)
   - Image upscaling

3. **UI Enhancements**
   - Gallery view of past generations
   - Prompt history and favorites
   - Batch prompt processing
   - Advanced parameter presets

4. **Performance Optimizations**
   - Model quantization for faster CPU
   - Multi-GPU support
   - Cached model loading
   - Progressive generation preview

5. **Additional Styles**
   - More style presets
   - Style mixing
   - Custom style training

## 🔧 Troubleshooting

### Common Issues

**Issue: Model download fails**
```
Solution: 
- Check internet connection
- Ensure 10+ GB free space
- Re-run the download (it will resume)
- Try a different network
```

**Issue: Out of memory error (CUDA)**
```
Solution:
- Reduce image dimensions (try 512×512)
- Generate fewer images at once
- Reduce inference steps
- Enable attention slicing (already enabled)
```

**Issue: CPU generation is very slow**
```
Solution:
- Reduce inference steps to 20-30
- Use 512×512 resolution
- Generate one image at a time
- Consider using Google Colab for GPU access
```

**Issue: Generated images are low quality**
```
Solution:
- Increase inference steps (50-70)
- Improve prompt with quality descriptors
- Adjust guidance scale (try 7-15)
- Use negative prompts
- Try different style presets
```

**Issue: Import errors**
```
Solution:
pip install -r requirements.txt --upgrade
```

### Getting Help

- Check existing issues in documentation
- Review prompt engineering guide
- Ensure all dependencies are installed
- Verify model downloaded correctly

## 📄 License

This project uses open-source components:

- **Stable Diffusion**: CreativeML OpenRAIL-M License
- **Code**: MIT License (see LICENSE file)

## 🙏 Acknowledgments

- [Stability AI](https://stability.ai/) - Stable Diffusion models
- [Hugging Face](https://huggingface.co/) - Diffusers library
- [Streamlit](https://streamlit.io/) - Web framework

## 📞 Support

For issues and questions:
1. Review this README thoroughly
2. Check the Troubleshooting section
3. Experiment with different settings
4. Consult online Stable Diffusion communities

---

**Made with ❤️ using open-source AI technology**

*Remember: With great AI power comes great responsibility. Use ethically!*
