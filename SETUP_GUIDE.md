# Setup Guide - AI Image Generator

## 🚀 Quick Start (5 Minutes)

### Option 1: Basic Setup (CPU)

1. **Install Python** (if not already installed)
   - Download from [python.org](https://python.org)
   - Version 3.8 or higher required
   - Make sure to check "Add Python to PATH"

2. **Open Terminal/Command Prompt**
   ```bash
   cd "c:\Users\ARNAV\OneDrive\Desktop\ML Task"
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Model**
   ```bash
   python utils/model_downloader.py
   ```
   - Select option 1 (Stable Diffusion v1.5 - Recommended)
   - Wait for download (~4 GB, 5-15 minutes)

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

6. **Open Browser**
   - App opens automatically at `http://localhost:8501`
   - Click "Load Model" in sidebar
   - Start generating!

### Option 2: GPU Setup (NVIDIA)

If you have an NVIDIA GPU, follow these steps for much faster generation:

1. **Check GPU Compatibility**
   ```bash
   nvidia-smi
   ```
   - You should see your GPU listed
   - Need 6+ GB VRAM recommended

2. **Install CUDA-enabled PyTorch**
   ```bash
   # For CUDA 11.8
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   
   # For CUDA 12.1
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

3. **Install Other Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Model and Run** (same as CPU option)
   ```bash
   python utils/model_downloader.py
   streamlit run app.py
   ```

## 📋 Detailed Installation

### Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

Expected output:
- PyTorch version (e.g., 2.0.0)
- CUDA available: True (if GPU) or False (if CPU)

## 🔧 Advanced Configuration

### Using Google Colab (Free GPU)

If you don't have a local GPU, use Google Colab:

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Create new notebook
3. Copy this setup code:

```python
# Install dependencies
!pip install -q torch diffusers transformers accelerate streamlit

# Clone repository (or upload files)
# ... add your files ...

# Run with ngrok for public URL
!pip install -q pyngrok
!ngrok authtoken YOUR_TOKEN  # Get free token from ngrok.com

# Run streamlit
!streamlit run app.py & npx localtunnel --port 8501
```

### Cloud Deployment

For permanent deployment:

**Hugging Face Spaces:**
1. Create account at huggingface.co
2. Create new Space (Streamlit)
3. Upload all files
4. Auto-deploys!

**Streamlit Cloud:**
1. Push code to GitHub
2. Connect at share.streamlit.io
3. Deploy (free tier available)

## 🐛 Troubleshooting Setup

### Issue: pip not found
```bash
# Windows
py -m pip install -r requirements.txt

# Or use full path
python -m pip install -r requirements.txt
```

### Issue: Permission denied
```bash
# Windows (Run as Administrator)
# Or use --user flag
pip install --user -r requirements.txt
```

### Issue: SSL Certificate Error
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Issue: Dependency conflicts
```bash
# Create fresh virtual environment
python -m venv fresh_venv
fresh_venv\Scripts\activate  # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Model download fails

**Solution 1: Manual download**
1. Go to [huggingface.co/runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5)
2. Download model files
3. Place in `~/.cache/huggingface/hub/`

**Solution 2: Use different network**
- Try different WiFi/internet connection
- Download will resume if interrupted

**Solution 3: Use smaller model**
```python
# In app.py, use a smaller model for testing
"CompVis/stable-diffusion-v1-4"  # Slightly smaller
```

## 📊 System Check

Run this to verify everything is working:

```python
# check_system.py
import sys
import torch
from diffusers import StableDiffusionPipeline

print("=== System Check ===")
print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

print("\nAttempting to load model...")
try:
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
```

Save as `check_system.py` and run:
```bash
python check_system.py
```

## 🎯 First Run Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`requirements.txt`)
- [ ] Model downloaded (4-7 GB)
- [ ] Streamlit running (`streamlit run app.py`)
- [ ] Browser opened at localhost:8501
- [ ] Model loaded in app (click "Load Model")
- [ ] Test generation works

## 💾 Storage Requirements

- **Python + Dependencies**: ~2 GB
- **Stable Diffusion v1.5**: ~4 GB
- **Stable Diffusion v2.1**: ~5 GB
- **Generated images**: Variable (100 MB per 100 images avg)
- **Total recommended**: 15 GB free space

## ⚡ Performance Optimization

### For CPU Users
```python
# In app.py, reduce default settings:
DEFAULT_INFERENCE_STEPS = 25  # Instead of 50
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
```

### For GPU Users
```python
# Already optimized with:
- attention slicing
- VAE slicing
- float16 precision
- DPM-Solver scheduler
```

### Memory Management
```python
# If running out of memory:
1. Generate one image at a time
2. Use 512x512 resolution
3. Reduce inference steps to 30
4. Close other applications
```

## 📚 Learning Path

1. **Day 1**: Basic setup and first generation
2. **Day 2**: Experiment with prompts
3. **Day 3**: Try different styles
4. **Day 4**: Master negative prompts
5. **Day 5**: Advanced parameters (guidance, steps, seed)

## 🆘 Getting Help

1. Check README.md troubleshooting section
2. Review this setup guide
3. Verify all dependencies installed correctly
4. Check GitHub issues for similar problems
5. Join Stable Diffusion community forums

---

**Ready to create? Run `streamlit run app.py` and start generating! 🎨**
