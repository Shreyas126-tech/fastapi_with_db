import os
import time
from utils.image_gen import generate_image
from dotenv import load_dotenv

load_dotenv('.env')

def verify_hyper_robust():
    print("Testing hyper-robust generation...")
    # Test with a prompt that should trigger fallback if API is down
    prompt = "A high-tech laboratory with glowing blue lights"
    try:
        image_path = generate_image(prompt)
        print(f"Result URL/Path: {image_path}")
        
        if image_path.startswith('http'):
            print("Verified: System correctly fell back to external CDN URL.")
        else:
            full_path = image_path.lstrip('/')
            if os.path.exists(full_path):
                print(f"Verified: System successfully saved image to local path: {full_path}")
            else:
                print(f"ERROR: Returned path {full_path} does not exist on disk.")
    except Exception as e:
        print(f"Hyper-robust test failed catastrophically: {e}")

if __name__ == "__main__":
    verify_hyper_robust()
