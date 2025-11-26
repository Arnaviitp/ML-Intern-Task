# 📊 Project Structure & Technical Documentation

## 🗂️ Directory Structure

```
ML Task/
│
├── 📄 app.py                          # Main Streamlit application (17.7 KB)
├── 📄 requirements.txt                # Python dependencies
├── 📄 verify_setup.py                 # Setup verification script
│
├── 📘 README.md                       # Complete documentation
├── 📘 QUICKSTART.md                   # 5-minute start guide
├── 📘 SETUP_GUIDE.md                  # Detailed installation
├── 📘 PROMPT_GUIDE.md                 # Prompt engineering examples
├── 📘 PROJECT_STRUCTURE.md            # This file
│
├── 🪟 install.bat                     # Windows installation script
├── 🪟 run_app.bat                     # Windows run script
│
├── 📁 utils/                          # Utility modules
│   ├── __init__.py                   # Package initializer
│   ├── config.py                     # Configuration settings
│   ├── prompt_engineer.py            # Prompt enhancement
│   ├── content_filter.py             # Safety filtering
│   ├── image_processor.py            # Image processing
│   └── model_downloader.py           # Model download utility
│
├── 📁 generated_images/               # Output directory (auto-created)
│   └── .gitkeep
│
└── 📄 .gitignore                      # Git ignore rules
```

## 📦 Core Components

### 1. Main Application (`app.py`)

**Purpose**: Streamlit web interface for image generation

**Key Features**:
- Model loading and initialization
- User interface with sidebar controls
- Real-time generation with progress tracking
- Image display and download
- Metadata tracking
- Session state management

**Main Classes**:
- `ImageGenerator`: Core generation logic
  - `_detect_device()`: GPU/CPU detection
  - `load_model()`: Model initialization
  - `generate_images()`: Image generation pipeline
  - `save_images()`: Storage with metadata

**Technologies**:
- Streamlit for UI
- PyTorch for deep learning
- Diffusers for Stable Diffusion
- Custom CSS for styling

---

### 2. Configuration (`utils/config.py`)

**Purpose**: Centralized configuration management

**Settings Include**:
- Model defaults (SD v1.5)
- Generation parameters (512×512, steps=50, guidance=7.5)
- Style presets (9 built-in styles)
- Quality enhancers
- Negative prompt templates
- Watermark settings

**Key Constants**:
```python
DEFAULT_MODEL = "runwayml/stable-diffusion-v1-5"
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_INFERENCE_STEPS = 50
```

---

### 3. Prompt Engineer (`utils/prompt_engineer.py`)

**Purpose**: Enhance user prompts for better results

**Key Methods**:
- `enhance_prompt()`: Add quality descriptors
- `get_style_suffix()`: Apply style presets
- `extract_key_elements()`: Parse prompt components
- `generate_negative_prompt()`: Create negative prompts
- `suggest_improvements()`: Provide feedback
- `analyze_prompt()`: Comprehensive analysis
- `_calculate_completeness()`: Score prompts (0-100)

**Features**:
- Automatic quality enhancement
- Style application
- Prompt analysis and scoring
- Improvement suggestions
- Example templates

---

### 4. Content Filter (`utils/content_filter.py`)

**Purpose**: Ethical AI safeguards and content filtering

**Key Methods**:
- `is_safe()`: Basic safety check
- `check_prompt()`: Detailed checking with feedback
- `_might_contain_real_person()`: Person detection
- `sanitize_prompt()`: Remove problematic content
- `get_filter_report()`: Detailed analysis

**Safety Features**:
- Blocked keyword detection
- Sensitive content warnings
- Real person detection (regex-based)
- Context-aware filtering
- Sanitization options

**Ethical Guidelines**:
- Acceptable use cases
- Prohibited content
- Best practices
- Privacy considerations
- Responsibility framework

---

### 5. Image Processor (`utils/image_processor.py`)

**Purpose**: Image manipulation and enhancement

**Key Methods**:
- `add_watermark()`: Add "AI Generated" watermark
- `resize_image()`: Resize with aspect ratio
- `enhance_image()`: Brightness, contrast, sharpness, saturation
- `convert_format()`: Format conversion (PNG, JPEG, WEBP)
- `create_thumbnail()`: Generate thumbnails
- `apply_filter()`: Predefined filters (vintage, vibrant, soft, dramatic)

**Watermarking**:
- Configurable text and opacity
- Multiple position options
- Semi-transparent overlay
- Format preservation

---

### 6. Model Downloader (`utils/model_downloader.py`)

**Purpose**: Download and manage AI models

**Key Features**:
- Interactive model selection
- Progress tracking
- Resume capability
- Cache management
- Model listing

**Supported Models**:
1. Stable Diffusion v1.5 (~4 GB) - Recommended
2. Stable Diffusion v2.1 (~5 GB) - Advanced

**Methods**:
- `download_model()`: Download from Hugging Face
- `check_model_exists()`: Verify local models
- `list_downloaded_models()`: Show cached models

---

## 🔄 Application Flow

### Initialization Flow
```
1. User runs: streamlit run app.py
2. Streamlit loads app.py
3. Custom CSS applied
4. ImageGenerator initialized
   ├── Config loaded
   ├── ContentFilter created
   ├── PromptEngineer created
   ├── ImageProcessor created
   └── Device detected (GPU/CPU)
5. UI rendered
   ├── Sidebar controls
   └── Main content area
6. User clicks "Load Model"
7. Model downloaded/cached and loaded into memory
8. Ready for generation
```

### Generation Flow
```
1. User enters prompt
2. User adjusts parameters (optional)
3. User clicks "Generate Images"
4. Content filtering
   ├── Check for inappropriate content
   └── Block if unsafe
5. Prompt engineering
   ├── Enhance with quality descriptors
   └── Apply style if selected
6. Generation loop (for each image)
   ├── Set seed if specified
   ├── Call Stable Diffusion pipeline
   ├── Progress bar update
   ├── Add watermark
   ├── Store metadata
   └── Clear cache
7. Display images
8. Provide download options
9. Save functionality (optional)
```

### Model Loading Flow
```
1. Check cache for existing model
2. If not found:
   ├── Download from Hugging Face (~4-7 GB)
   ├── Cache locally
   └── Track download progress
3. Load model to memory
4. Configure scheduler (DPM-Solver)
5. Move to device (GPU/CPU)
6. Enable optimizations:
   ├── Attention slicing
   ├── VAE slicing
   └── FP16 (if GPU)
7. Model ready
```

---

## 🎛️ Parameter Guide

### User-Facing Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| **Prompt** | Text | - | - | What to generate |
| **Negative Prompt** | Text | - | Default list | What to avoid |
| **Num Images** | Int | 1-4 | 1 | Images per prompt |
| **Guidance Scale** | Float | 1.0-20.0 | 7.5 | Prompt adherence |
| **Inference Steps** | Int | 10-100 | 50 | Quality vs speed |
| **Seed** | Int | 0-2147483647 | 0 (random) | Reproducibility |
| **Width** | Int | 512/768/1024 | 512 | Image width |
| **Height** | Int | 512/768/1024 | 512 | Image height |
| **Enhance Prompt** | Bool | - | True | Auto-enhance |
| **Style Preset** | Select | 10 options | None | Style to apply |
| **Format** | Select | PNG/JPEG | PNG | Export format |

### Internal Parameters

- `torch_dtype`: float16 (GPU) / float32 (CPU)
- `attention_slicing`: Enabled
- `vae_slicing`: Enabled
- `scheduler`: DPMSolverMultistepScheduler
- `safety_checker`: Disabled (custom filter used)

---

## 🧠 AI Model Details

### Stable Diffusion v1.5

**Architecture**: Latent Diffusion Model
- **Encoder**: VAE (Variational Autoencoder)
- **Denoiser**: U-Net with attention layers
- **Text Encoder**: CLIP ViT-L/14
- **Decoder**: VAE decoder

**Training**:
- Dataset: LAION-5B (filtered)
- Resolution: 512×512
- Parameters: ~890M
- Format: SafeTensors

**Inference Process**:
1. Text → CLIP embeddings
2. Random latent noise
3. Iterative denoising (50 steps default)
4. Latent → Image via VAE decoder
5. Post-processing

**Optimizations**:
- DPM-Solver: 2-3× faster than DDIM
- Attention slicing: Reduce memory usage
- VAE slicing: Process in tiles
- FP16: Half precision on GPU

---

## 📊 Performance Metrics

### Generation Times (Average)

**512×512, 50 steps:**
- RTX 4090: ~8 seconds
- RTX 3080: ~10 seconds
- RTX 3060: ~15 seconds
- GTX 1660: ~25 seconds
- CPU (i7): ~5 minutes
- CPU (i5): ~8 minutes

**768×768, 50 steps:**
- RTX 4090: ~15 seconds
- RTX 3080: ~20 seconds
- RTX 3060: ~30 seconds
- CPU (i7): ~12 minutes

### Memory Requirements

**512×512:**
- VRAM (GPU): 3-4 GB
- RAM (CPU): 8-10 GB

**768×768:**
- VRAM (GPU): 5-6 GB
- RAM (CPU): 12-14 GB

**1024×1024:**
- VRAM (GPU): 8-10 GB
- RAM (CPU): 16-20 GB

---

## 🔐 Security & Ethics

### Content Filtering Layers

1. **Pre-Generation**:
   - Keyword blocking
   - Pattern matching
   - Context analysis

2. **Post-Generation**:
   - Watermarking (all images)
   - Metadata tracking
   - Usage logging

### Privacy Considerations

- No data sent to external servers
- Models run locally
- No user data collection
- Metadata stored locally only

### Responsible AI

- Ethical guidelines included
- Usage restrictions documented
- Watermarking mandatory
- Content filtering enforced

---

## 🛠️ Development Notes

### Adding New Features

**New Style Preset**:
1. Add to `STYLE_PRESETS` in `config.py`
2. Style automatically available in UI

**New Model**:
1. Add to `model_options` in `app.py`
2. Ensure compatibility with Diffusers

**Custom Filter**:
1. Modify `content_filter.py`
2. Add keywords to blocked/sensitive lists

### Testing Checklist

- [ ] Model loads successfully
- [ ] Generation completes
- [ ] Watermark applied
- [ ] Metadata saved correctly
- [ ] Content filter works
- [ ] Download works
- [ ] Multiple images work
- [ ] Different sizes work
- [ ] CPU mode works
- [ ] GPU mode works

---

## 📈 Future Roadmap

### Phase 1 (Core Features)
- ✅ Basic text-to-image
- ✅ Multiple styles
- ✅ Content filtering
- ✅ Watermarking
- ✅ Metadata tracking

### Phase 2 (Enhanced Features)
- ⬜ Image-to-image
- ⬜ Inpainting
- ⬜ Outpainting
- ⬜ LoRA support
- ⬜ Multiple models

### Phase 3 (Advanced)
- ⬜ Fine-tuning interface
- ⬜ Custom training
- ⬜ Gallery system
- ⬜ Prompt library
- ⬜ Batch processing

### Phase 4 (Professional)
- ⬜ API endpoint
- ⬜ Multi-GPU support
- ⬜ Distributed generation
- ⬜ Cloud deployment
- ⬜ Mobile app

---

## 🔗 Dependencies Graph

```
app.py
├── streamlit (UI framework)
├── torch (Deep learning)
├── diffusers (Stable Diffusion)
│   ├── transformers
│   └── accelerate
├── PIL (Image processing)
└── utils/
    ├── config.py
    ├── prompt_engineer.py
    │   └── config.py
    ├── content_filter.py
    └── image_processor.py
        ├── PIL
        └── config.py
```

---

## 📝 License Information

- **Project Code**: MIT License
- **Stable Diffusion**: CreativeML OpenRAIL-M
- **Hugging Face Diffusers**: Apache 2.0
- **PyTorch**: BSD 3-Clause

---

**Last Updated**: 2025-11-26
**Version**: 1.0.0
**Python**: 3.8+
**Platform**: Windows/macOS/Linux
