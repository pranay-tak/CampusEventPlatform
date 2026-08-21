from PIL import Image, ImageDraw, ImageFont
import os

def overlay_event_text(image_path, event_details, output_path):
    """
    Overlays accurate text onto the AI-generated background.
    """
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Try to load a default font, fallback to basic if not available
        try:
            # Assuming a standard windows font or a bundled TTF
            title_font = ImageFont.truetype("arial.ttf", 60)
            text_font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Add a dark semi-transparent rectangle for readability
        overlay = Image.new('RGBA', img.size, (0,0,0,0))
        d_overlay = ImageDraw.Draw(overlay)
        d_overlay.rectangle([50, 50, img.width - 50, 400], fill=(0, 0, 0, 150))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)

        # Draw Title
        title = event_details.get("title", "Event Title")
        draw.text((80, 80), title, font=title_font, fill=(255, 255, 255))
        
        # Draw Details
        details = f"""
Date: {event_details.get('date', 'TBD')}
Time: {event_details.get('time', 'TBD')}
Venue: {event_details.get('venue', 'TBD')}
        """
        draw.text((80, 180), details, font=text_font, fill=(200, 200, 200))
        
        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Text overlay failed: {e}")
        return image_path
