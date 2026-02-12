import os
from utils.image_gen import generate_image
from dotenv import load_dotenv

load_dotenv('.env')

def test_image_gen():
    print("Testing image generation...")
    try:
        image_path = generate_image("A futuristic city at night, neon lights, rainy street")
        print(f"Result Path: {image_path}")
        full_path = image_path.lstrip('/')
        if os.path.exists(full_path):
            print(f"Verification Success: File {full_path} exists. Size: {os.path.getsize(full_path)} bytes")
        else:
            print(f"Verification Failure: File {full_path} NOT found.")
    except Exception as e:
        print(f"Test crashed: {e}")

if __name__ == "__main__":
    test_image_gen()
