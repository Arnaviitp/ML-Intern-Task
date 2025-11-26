"""
Model download and setup utility
"""

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download
from tqdm import tqdm


class ModelDownloader:
    """Download and manage AI models"""
    
    def __init__(self, cache_dir=None):
        """
        Initialize model downloader
        
        Args:
            cache_dir (str): Directory to cache models
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "huggingface"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def download_model(self, model_id, revision="main"):
        """
        Download a model from Hugging Face
        
        Args:
            model_id (str): Model identifier (e.g., "runwayml/stable-diffusion-v1-5")
            revision (str): Model revision/branch
        """
        print(f"\nDownloading model: {model_id}")
        print(f"Cache directory: {self.cache_dir}")
        print("\nThis may take several minutes depending on your internet speed...")
        print("The model is approximately 4-7 GB in size.\n")
        
        try:
            snapshot_download(
                repo_id=model_id,
                revision=revision,
                cache_dir=str(self.cache_dir),
                resume_download=True,
                local_files_only=False
            )
            
            print(f"\n✅ Successfully downloaded {model_id}")
            print(f"Model cached at: {self.cache_dir}")
            
        except Exception as e:
            print(f"\n❌ Error downloading model: {str(e)}")
            print("\nTroubleshooting tips:")
            print("1. Check your internet connection")
            print("2. Ensure you have enough disk space (~10 GB free)")
            print("3. Try again - the download will resume where it left off")
            print("4. If using a proxy, configure it properly")
            sys.exit(1)
    
    def check_model_exists(self, model_id):
        """
        Check if a model is already downloaded
        
        Args:
            model_id (str): Model identifier
            
        Returns:
            bool: True if model exists locally
        """
        # Simplified check - actual implementation would verify model files
        model_path = self.cache_dir / "hub" / f"models--{model_id.replace('/', '--')}"
        return model_path.exists()
    
    def list_downloaded_models(self):
        """List all downloaded models"""
        hub_dir = self.cache_dir / "hub"
        
        if not hub_dir.exists():
            print("No models downloaded yet.")
            return []
        
        models = []
        for item in hub_dir.iterdir():
            if item.is_dir() and item.name.startswith("models--"):
                model_name = item.name.replace("models--", "").replace("--", "/")
                size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                size_gb = size / (1024**3)
                models.append((model_name, size_gb))
        
        return models


def main():
    """Main function for standalone execution"""
    print("=" * 60)
    print("AI Image Generator - Model Downloader")
    print("=" * 60)
    
    downloader = ModelDownloader()
    
    # Check for existing models
    print("\nChecking for existing models...")
    existing_models = downloader.list_downloaded_models()
    
    if existing_models:
        print(f"\nFound {len(existing_models)} downloaded model(s):")
        for model_name, size_gb in existing_models:
            print(f"  • {model_name} ({size_gb:.2f} GB)")
    else:
        print("No models found.")
    
    print("\n" + "=" * 60)
    print("Available models to download:")
    print("=" * 60)
    
    models = {
        "1": {
            "name": "Stable Diffusion v1.5",
            "id": "runwayml/stable-diffusion-v1-5",
            "description": "Fast, good quality, widely compatible (Recommended)",
            "size": "~4 GB"
        },
        "2": {
            "name": "Stable Diffusion v2.1",
            "id": "stabilityai/stable-diffusion-2-1",
            "description": "Improved quality, larger model",
            "size": "~5 GB"
        },
    }
    
    for key, model in models.items():
        print(f"\n{key}. {model['name']}")
        print(f"   ID: {model['id']}")
        print(f"   Description: {model['description']}")
        print(f"   Size: {model['size']}")
    
    print("\n" + "=" * 60)
    choice = input("\nEnter the number of the model to download (or 'q' to quit): ").strip()
    
    if choice.lower() == 'q':
        print("Exiting...")
        return
    
    if choice not in models:
        print("Invalid choice!")
        return
    
    selected_model = models[choice]
    
    print(f"\nYou selected: {selected_model['name']}")
    confirm = input("Proceed with download? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Download cancelled.")
        return
    
    # Download the model
    downloader.download_model(selected_model['id'])
    
    print("\n" + "=" * 60)
    print("Setup complete! You can now run the main application:")
    print("  streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
