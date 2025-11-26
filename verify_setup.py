"""
Quick verification script to check if setup is complete
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro}")
        print("   Required: Python 3.8 or higher")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = {
        'torch': 'PyTorch',
        'diffusers': 'Diffusers',
        'transformers': 'Transformers',
        'streamlit': 'Streamlit',
        'PIL': 'Pillow'
    }
    
    all_installed = True
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - Not installed")
            all_installed = False
    
    return all_installed


def check_cuda():
    """Check CUDA availability"""
    print("\n🎮 Checking GPU support...")
    
    try:
        import torch
        if torch.cuda.is_available():
            print(f"   ✅ CUDA available")
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        else:
            print("   ⚠️  CUDA not available (will use CPU)")
            print("   Note: Generation will be slower on CPU")
    except:
        print("   ❌ Could not check CUDA")


def check_model():
    """Check if model is downloaded"""
    print("\n🤖 Checking for downloaded models...")
    
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    
    if cache_dir.exists():
        models = [
            d for d in cache_dir.iterdir() 
            if d.is_dir() and d.name.startswith("models--")
        ]
        
        if models:
            print(f"   ✅ Found {len(models)} model(s)")
            for model in models:
                model_name = model.name.replace("models--", "").replace("--", "/")
                print(f"      • {model_name}")
        else:
            print("   ⚠️  No models downloaded yet")
            print("   Run: python utils/model_downloader.py")
    else:
        print("   ⚠️  Model cache directory not found")
        print("   Run: python utils/model_downloader.py")


def check_project_structure():
    """Check if all required files exist"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "utils/__init__.py",
        "utils/config.py",
        "utils/prompt_engineer.py",
        "utils/content_filter.py",
        "utils/image_processor.py",
        "utils/model_downloader.py"
    ]
    
    all_exist = True
    
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - Missing")
            all_exist = False
    
    return all_exist


def check_output_directory():
    """Check if output directory exists"""
    print("\n💾 Checking output directory...")
    
    output_dir = Path("generated_images")
    if output_dir.exists():
        print(f"   ✅ Output directory exists")
    else:
        print(f"   Creating output directory...")
        output_dir.mkdir(exist_ok=True)
        print(f"   ✅ Created output directory")


def main():
    """Main verification function"""
    print("=" * 60)
    print("AI Image Generator - Setup Verification")
    print("=" * 60)
    
    checks = []
    
    # Run all checks
    checks.append(("Python Version", check_python_version()))
    checks.append(("Project Structure", check_project_structure()))
    checks.append(("Dependencies", check_dependencies()))
    
    check_cuda()
    check_model()
    check_output_directory()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = all(result for _, result in checks)
    
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ All critical checks passed!")
        print("\nNext steps:")
        print("1. If no model downloaded: python utils/model_downloader.py")
        print("2. Start the application: streamlit run app.py")
    else:
        print("⚠️  Some checks failed.")
        print("\nPlease fix the issues above before running the application.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
