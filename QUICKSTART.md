# 🚀 QUICKSTART - Get Running in 5 Minutes

## For Windows Users (Easiest Method)

### 1️⃣ Install (One Time Only)
Double-click `install.bat` and wait for completion.

### 2️⃣ Download AI Model (One Time Only)
```bash
python utils\model_downloader.py
```
Select option 1 (Stable Diffusion v1.5) and wait for download.

### 3️⃣ Run Application
Double-click `run_app.bat`

Your browser will open automatically!

---

## For All Users (Command Line)

### Quick Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Download model
python utils/model_downloader.py

# Verify setup
python verify_setup.py

# Run application
streamlit run app.py
```

---

## First Time Usage

1. **Load Model**: Click "Load Model" button in sidebar (takes 30-60 seconds)
2. **Enter Prompt**: Type what you want to create
3. **Generate**: Click "Generate Images" button
4. **Download**: Click download button below generated image

---

## Example First Prompt

Try this for your first image:
```
Beautiful sunset over mountains, golden hour lighting, 
professional photography, highly detailed, 8k
```

---

## Quick Settings

**Fast generation (lower quality):**
- Inference Steps: 20-30
- Size: 512×512

**High quality (slower):**
- Inference Steps: 50-70
- Size: 768×768

---

## Need Help?

- **Full Guide**: See `README.md`
- **Setup Issues**: See `SETUP_GUIDE.md`
- **Better Prompts**: See `PROMPT_GUIDE.md`
- **Check Setup**: Run `python verify_setup.py`

---

## Common First-Time Issues

**"Model not found"**
→ Run `python utils/model_downloader.py` first

**"Out of memory"**
→ Reduce image size to 512×512 and steps to 20

**"Very slow"**
→ Normal on CPU - expect 3-10 minutes per image

---

**🎨 Happy Creating!**
