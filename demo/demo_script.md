# Demo Video Script (3-5 Minutes)

**0:00–0:20 | Introduction**
"Hello, my name is Pranay Tak. This is my AI-Powered Campus Event Discovery platform. The problem is that university events are scattered across notice boards and WhatsApp. My solution centralizes this using 100% Local AI."

**0:20–0:45 | Dashboard**
"Here is the student dashboard where upcoming events are displayed. But let's look at how these events are created."

**0:45–1:30 | Organizer Portal & Upload**
"I'll switch to the Organizer view. An organizer usually has a basic poster. I upload it here." *(Upload sample image)*

**1:30–2:00 | OCR & Local LLM**
"The system uses EasyOCR locally to extract text. Then, it sends this messy text to my Local LLM, Ollama running Llama 3.2. You can see the LLM structured the data perfectly into JSON."

**2:00–2:30 | AI Content Generation**
"The LLM also automatically generated an Instagram caption, an email announcement, and hashtags for the organizer."

**2:30–3:00 | Local Image Generation**
"Next, the LLM creates an image prompt. The system uses a local image generation setup to create a beautiful, modern background. Then, Python overlays the exact event text onto the image so there are no spelling errors."

**3:00–3:30 | Final Poster**
"Here is the final generated poster. We click Publish."

**3:30–4:30 | Student Discovery & Search**
"Back as a student, I can search naturally: 'Show me AI events this weekend'. The LLM translates this to a database query, and here are the results from SQLite."

**4:30–5:00 | Conclusion**
"Everything ran locally on this machine without OpenAI or any cloud APIs. Thank you."
