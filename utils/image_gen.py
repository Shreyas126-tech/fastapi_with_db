import os
import requests
import base64
import time
from dotenv import load_dotenv

# Get the path to the root directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
API_URL = "https://models.inference.ai.azure.com/images/generations"
IMAGE_MODEL = "stable-diffusion-xl" # Common Azure/GH model ID

# Create static/generated_images directory if it doesn't exist
IMAGES_DIR = os.path.join(base_dir, 'static', 'generated_images')
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def generate_image(prompt: str) -> str:
    """
    Generate an image using GitHub Models with rotation and hyper-robust fallback.
    """
    filename = f"gen_{int(time.time())}.png"
    filepath = os.path.join(IMAGES_DIR, filename)
    
    # Try these model IDs in order
    model_ids = [
        "stability-ai/sdxl",
        "black-forest-labs/flux-1-schnell",
        "stability-ai/stable-diffusion-3-5-large"
    ]

    for model_id in model_ids:
        try:
            if not GITHUB_TOKEN:
                break

            headers = {
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": prompt,
                "model": model_id,
                "n": 1,
                "size": "1024x1024",
                "response_format": "b64_json"
            }

            print(f"Attempting GitHub Models: {model_id}")
            response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                b64_data = data['data'][0]['b64_json']
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(b64_data))
                return f"/static/generated_images/{filename}"
            else:
                print(f"GitHub {model_id} failed: {response.status_code}")
                continue # Try next model

        except Exception as e:
            print(f"GitHub {model_id} error: {e}")
            continue

    # SMART FALLBACK: Use Pollinations.ai - prompt-aware
    try:
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)
        # Use different seeds to avoid caching
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={int(time.time())}"
        
        print(f"Trying Smart Fallback (Pollinations.ai)...")
        r = requests.get(pollinations_url, timeout=25)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            return f"/static/generated_images/{filename}"
    except Exception as fallback_err:
        print(f"Smart Fallback failed: {fallback_err}")
            
    # ABSOLUTE LAST RESORT: Check if not_found.png exists, otherwise use a direct CDN link
    local_not_found = os.path.join(IMAGES_DIR, "not_found.png")
    if os.path.exists(local_not_found):
        return "/static/generated_images/not_found.png"
    
    return "https://images.unsplash.com/photo-1614064641935-3bb7ce99cc3a?q=80&w=1024"
