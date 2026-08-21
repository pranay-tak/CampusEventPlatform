# Viva Preparation Guide

## General
**Q: What problem does your project solve?**
**A:** It centralizes fragmented campus event information. Students miss events because info is scattered across WhatsApp, notice boards, and emails. Organizers waste time recreating promotional material. This platform solves both through a centralized hub and AI automation.

**Q: What makes your project AI-powered?**
**A:** It uses artificial intelligence for OCR (extracting text from posters), Natural Language Processing (structuring event data and interpreting natural language searches via an LLM), and Generative AI (creating captions and event background images).

## Local LLM
**Q: What is an LLM and why use a local one?**
**A:** A Large Language Model understands and generates human-like text. A local LLM (like Llama 3.2 via Ollama) guarantees privacy, costs nothing per API call, and proves full control over the AI stack, completely avoiding cloud dependencies (OpenAI/Gemini).

**Q: How does the LLM interact with your application?**
**A:** I send HTTP POST requests to Ollama's local REST API (`http://localhost:11434/api/generate`) with specific system prompts to force JSON output for structuring, or creative prompts for generating captions.

## Image Generation
**Q: How does the image generation work locally?**
**A:** The platform is designed to connect to a local ComfyUI API endpoint. The LLM generates a descriptive prompt, which is sent to ComfyUI (running Stable Diffusion/FLUX). To ensure exact text on the poster (since image models struggle with spelling), I use Python's Pillow library to deterministically overlay the event title and details onto the AI-generated background.

## Architecture & Search
**Q: How does natural-language search work? Does the LLM invent the events?**
**A:** No. The LLM simply translates the user's natural language query (e.g., "AI events today") into structured search parameters (e.g., `{"category": "AI", "time": "today"}`). The application then uses these parameters to query the deterministic SQLite database. This prevents hallucinations and ensures users only see real, scheduled events.
