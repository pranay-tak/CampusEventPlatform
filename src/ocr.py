import os
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
import logging

def extract_text_from_image(image_path):
    """
    Extracts text from an uploaded poster using local EasyOCR.
    """
    if not EASYOCR_AVAILABLE:
        logging.warning("EasyOCR not installed. Returning empty text.")
        return ""
        
    try:
        # Initialize reader (will use GPU if available, else CPU)
        reader = easyocr.Reader(['en'], gpu=False) # Defaulting to CPU for broader compatibility on student laptops
        results = reader.readtext(image_path)
        
        extracted_text = " ".join([res[1] for res in results])
        return extracted_text
    except Exception as e:
        logging.error(f"OCR Error: {e}")
        return f"Error running OCR: {e}"
