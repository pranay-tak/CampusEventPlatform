import requests
import json
import logging
import os
import random
from PIL import Image, ImageDraw

COMFYUI_URL = "http://localhost:8188/prompt"

def generate_image_comfyui(prompt, output_filename="generated_poster.png"):
    """
    Sends a generation request to a local ComfyUI API.
    Note: ComfyUI requires a specific JSON workflow format.
    For simplicity in this academic MVP, we simulate the output if ComfyUI isn't running,
    or provide the exact stub where the ComfyUI API call goes.
    """
    # A standard ComfyUI workflow JSON goes here.
    # We will use a mock/fallback generation if the API isn't reachable.
    
    try:
        # Check if ComfyUI is up
        requests.get("http://localhost:8188", timeout=2)
        # If reachable, you would post the workflow payload here.
        # ...
        logging.info("ComfyUI reachable. (Stub for actual generation)")
        # Simulate saving the image
        img = _generate_mock_image(prompt)
        os.makedirs("outputs/generated_posters", exist_ok=True)
        path = f"outputs/generated_posters/{output_filename}"
        img.save(path)
        return path
    except requests.exceptions.RequestException:
        logging.warning("ComfyUI not running. Falling back to local Python mock generation to demonstrate workflow.")
        img = _generate_mock_image(prompt)
        os.makedirs("outputs/generated_posters", exist_ok=True)
        path = f"outputs/generated_posters/fallback_{output_filename}"
        img.save(path)
        return path

def _generate_mock_image(prompt):
    """
    Generates a placeholder image visually representing the 'local generation' concept
    when GPU/ComfyUI is not available on a student's laptop.
    """
    width, height = 800, 1000
    color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    img = Image.new('RGB', (width, height), color=color)
    d = ImageDraw.Draw(img)
    d.text((50, height//2), f"AI GENERATED BACKGROUND\nPrompt:\n{prompt[:100]}...", fill=(255, 255, 255))
    return img
