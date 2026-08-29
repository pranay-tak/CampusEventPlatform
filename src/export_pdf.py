from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def generate_event_pdf(event_details, output_path="outputs/event_export.pdf"):
    """
    Generates a PDF for a given event.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, event_details.get('title', 'Event Title'))
    
    # Event Image
    poster_path = event_details.get('generated_poster_path')
    if poster_path and os.path.exists(poster_path):
        try:
            img = ImageReader(poster_path)
            # Draw image keeping aspect ratio roughly (width: 500, height: variable)
            c.drawImage(img, 50, height - 400, width=500, height=300, preserveAspectRatio=True)
        except Exception as e:
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 100, f"[Image rendering failed: {e}]")
            
    # Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 450, "Event Details:")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 475, f"Date: {event_details.get('date', 'TBD')}")
    c.drawString(50, height - 495, f"Time: {event_details.get('start_time', 'TBD')}")
    c.drawString(50, height - 515, f"Venue: {event_details.get('venue', 'TBD')}")
    c.drawString(50, height - 535, f"Category: {event_details.get('category', 'TBD')}")
    
    c.drawString(50, height - 565, "Description:")
    
    # Handle description wrapping
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph
    styles = getSampleStyleSheet()
    p = Paragraph(event_details.get('description', ''), styles['Normal'])
    p.wrapOn(c, 500, 200)
    p.drawOn(c, 50, height - 650)
    
    c.save()
    return output_path
