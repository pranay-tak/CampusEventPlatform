import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2"

def generate_text(prompt, model=DEFAULT_MODEL, system_prompt=None):
    """Generates text using local Ollama instance."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    if system_prompt:
        payload["system"] = system_prompt
        
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        logging.error(f"Error communicating with Ollama: {e}")
        return f"Error: Could not reach Local LLM (Ollama). Details: {e}"

def extract_structured_event_data(raw_text, model=DEFAULT_MODEL):
    """Uses LLM to structure raw OCR text into JSON format."""
    system_prompt = "You are a helpful AI assistant. Your task is to extract event details from raw text and format it as a JSON object with keys: title, description, category, date, time, venue, registration, contact, tags (list of strings)."
    prompt = f"Extract the event details from this text and return ONLY valid JSON:\n\n{raw_text}"
    
    response = generate_text(prompt, model=model, system_prompt=system_prompt)
    
    # Try to clean the response to get just the JSON block
    try:
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_str = response.split("```")[1].strip()
        else:
            json_str = response.strip()
        return json.loads(json_str)
    except Exception as e:
        logging.error(f"Failed to parse LLM JSON: {e}")
        return {"error": "Failed to parse JSON", "raw": response}

def generate_social_captions(event_details, model=DEFAULT_MODEL):
    """Generates Instagram and LinkedIn captions."""
    prompt = f"""
    Event Details:
    Title: {event_details.get('title')}
    Description: {event_details.get('description')}
    Date/Time: {event_details.get('date')} {event_details.get('time')}
    Venue: {event_details.get('venue')}
    
    Output exactly two captions separated by "---":
    
    1) Instagram: hook line, key details, 3-5 hashtags, casual/energetic, under 150 words.
    ---
    2) LinkedIn: formal tone, value/opportunity framed, no excessive hashtags, under 120 words.
    """
    
    response = generate_text(prompt, model=model)
    parts = response.split("---")
    
    ig = parts[0].strip() if len(parts) > 0 else response
    li = parts[1].strip() if len(parts) > 1 else "Error generating LinkedIn caption."
    
    return {"instagram": ig, "linkedin": li}

def generate_image_prompt(event_details, model=DEFAULT_MODEL):
    """Generates a prompt for the Image Generation Model."""
    prompt = f"""
    Create a highly detailed image generation prompt for an event poster.
    Event: {event_details.get('title')}
    Category: {event_details.get('category')}
    Description: {event_details.get('description')}
    
    The prompt should describe a modern, professional university poster background suitable for this event. 
    It should include styling, lighting, and composition details. No text in the image.
    Just return the image generation prompt string.
    """
    return generate_text(prompt, model=model)
