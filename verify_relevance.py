import os
import time
from utils.image_gen import generate_image
from dotenv import load_dotenv

load_dotenv('.env')

def verify_relevance():
    print("Testing relevance with a specific prompt...")
    prompt = "A cute yellow cat wearing a tiny top hat and holding a red rose"
    try:
        image_path = generate_image(prompt)
        print(f"Result Path: {image_path}")
        # Check if file exists and has content
        full_path = image_path.lstrip('/')
        if os.path.exists(full_path) and os.path.getsize(full_path) > 1000:
            print(f"SUCCESS: Image generated and saved. File: {full_path}")
            print("Note: If you see a nature image, it's still failing. If you see a CAT, the smart fallback (Pollinations) is working perfectly.")
        else:
            print("FAILURE: File not found or empty.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_relevance()
