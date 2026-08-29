import requests
import json
import logging
import os
import random
from PIL import Image, ImageDraw

A1111_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

def generate_image_a1111(prompt, output_filename="generated_poster.png"):
    """
    Sends a generation request to a local AUTOMATIC1111 API.
    Designed to work on CPU with flags: --no-half --skip-torch-cuda-test
    """
    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 800,
        "height": 1000,
        "sampler_name": "Euler a",
        "override_settings": {
            "sd_model_checkpoint": "v1-5-pruned-emaonly.safetensors"
        }
    }
    
    try:
        logging.info("Attempting to connect to AUTOMATIC1111 API...")
        response = requests.post(A1111_URL, json=payload, timeout=5)
        response.raise_for_status()
        
        # Save base64 image
        import base64
        import io
        r = response.json()
        img_data = base64.b64decode(r['images'][0])
        img = Image.open(io.BytesIO(img_data))
        
        os.makedirs("outputs/generated_posters", exist_ok=True)
        path = f"outputs/generated_posters/{output_filename}"
        img.save(path)
        return path
    except requests.exceptions.RequestException as e:
        logging.warning(f"AUTOMATIC1111 not running or failed ({e}). Falling back to local mock generator.")
        img = _generate_mock_image(prompt)
        os.makedirs("outputs/generated_posters", exist_ok=True)
        path = f"outputs/generated_posters/fallback_{output_filename}"
        img.save(path)
        return path

def _generate_mock_image(prompt):
    """
    Generates a clean placeholder image gradient.
    """
    width, height = 800, 1000
    color1 = (random.randint(50, 150), random.randint(50, 150), random.randint(100, 200))
    color2 = (random.randint(20, 80), random.randint(20, 80), random.randint(50, 100))
    
    img = Image.new('RGB', (width, height), color=color1)
    d = ImageDraw.Draw(img)
    # Simple top-to-bottom gradient
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * (y / height))
        g = int(color1[1] + (color2[1] - color1[1]) * (y / height))
        b = int(color1[2] + (color2[2] - color1[2]) * (y / height))
        d.line([(0, y), (width, y)], fill=(r, g, b))
        
    return img
