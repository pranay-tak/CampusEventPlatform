# AI-Powered Campus Event Discovery Platform

## 1. Project Overview
A centralized AI-powered campus event platform designed to solve event-discovery blind spots at CHRIST (Deemed to be University), Bengaluru Central Campus.

**By:** Pranay Tak  
**Program:** M.Sc. Data Analytics

## 2. Problem Statement
Campus events are highly fragmented. Students rely on physical notice boards, WhatsApp groups, and varied social media accounts, leading to missed opportunities. Organizers repeatedly perform manual promotional work with poor targeting.

## 3. Proposed Solution
A two-sided application where:
1. **Organizers** upload event posters. A local AI workflow extracts details, generates promotional text (captions, emails), and synthesizes a modern background poster.
2. **Students** discover events using natural language search and receive personalized recommendations.

## 4. Key Features
*   **Student Features**: Natural language search, Personalized event recommendations.
*   **Organizer Features**: Automated event creation, AI content generation, AI poster design.
*   **AI Features**: Local OCR, Local LLM structuring/generation, Local Image Generation.

## 5. Local AI Models 
*   **Local LLM**: `llama3.2` running via **Ollama**. Selected for its excellent instruction-following capabilities while remaining feasible for consumer laptops.
*   **Local Image Generation**: Local ComfyUI / Diffusers API. Keeps visual synthesis entirely local.
*   **OCR**: `EasyOCR` or `Tesseract` for local text extraction from images.

## 6. Architecture
*(See `docs/architecture.png`)*
The application is a Streamlit frontend interfacing with a SQLite database. Python modules handle interactions with local AI services (Ollama, ComfyUI).

## 7. AI Workflow
Upload Poster -> OCR -> Local LLM (Structure Data) -> Local LLM (Generate Content & Image Prompt) -> Local Image Model (Generate Background) -> Pillow (Text Overlay) -> Final Poster.

## 8. Natural Language Search
The Local LLM interprets queries (e.g., "AI workshops this weekend") and maps them to structured JSON filters, which are then used to query the local SQLite database.

## 9. Recommendation System
A content-based recommendation engine scoring events based on:
* Interest/category match (40%)
* Tags match (25%)
* Past interactions (20%)

## 10. Technology Stack
| Component | Technology |
| :--- | :--- |
| Frontend/UI | Streamlit |
| Backend | Python 3.10+ |
| Database | SQLite |
| Local LLM | Ollama (`llama3.2`) |
| Image Generation | ComfyUI API Stub |
| OCR | EasyOCR |

## 11. Repository Structure
*   `app.py`: Main Streamlit application.
*   `src/`: Core logic (db, llm, ocr, image_gen, search, recommendations).
*   `data/`: SQLite DB and sample JSON data.
*   `outputs/`: Generated posters.

## 12. Hardware Requirements
*   **Minimum**: CPU-only, 16GB RAM (Ollama will run slower, Image Generation will use mock/fallback).
*   **Recommended**: NVIDIA GPU (6GB+ VRAM) for hardware-accelerated EasyOCR and fast local model inference.

## 13. Installation
```bash
git clone <repo-url>
cd CampusEventPlatform
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 14. Configuration
1. Install [Ollama](https://ollama.com/) locally.
2. Run `ollama run llama3.2` in terminal to download the model.
3. Ensure ComfyUI is running on port 8188 (if using real GPU image generation, otherwise the app falls back to a visual placeholder).

## 15. Running the Application
```bash
streamlit run app.py
```

## 16. Demo Workflow
See `demo/demo_script.md` for the exact steps to demonstrate the AI capabilities.

## 19. Privacy
**100% Local.** No student data or event information is sent to OpenAI, Google, or any cloud provider.

## 20. Limitations
*   Local LLM might hallucinate JSON structures occasionally.
*   Image generation without a GPU defaults to a stylized placeholder.

## 21. Future Scope
Cross-campus discovery, Calendar integration, Attendance prediction.


