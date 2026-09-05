# AI-Powered Campus Event Discovery Platform

## 1. Project Overview
A centralized AI-powered campus event platform designed to solve event-discovery blind spots at CHRIST (Deemed to be University), Bengaluru Central Campus.

**By:** Pranay Tak  
**Program:** M.Sc. Data Analytics

## 2. Problem Statement
Campus events are highly fragmented. Students rely on physical notice boards, WhatsApp groups, and varied social media accounts, leading to missed opportunities. Organizers repeatedly perform manual promotional work with poor targeting.

## 3. Proposed Solution
A two-sided application where:
1. **Organizers** upload event posters (or manually enter details). A local AI workflow extracts details, generates promotional text (Instagram/LinkedIn captions), and synthesizes a modern background poster.
2. **Students** discover events using SQL-backed filters and receive personalized "For You" recommendations based on their interests.

## 4. Repository Structure
```text
├── README.md              ← Professional documentation
├── LICENSE
├── .gitignore
├── requirements.txt
├── app.py
├── src/
├── docs/
│   ├── architecture.png
│   ├── workflow.png
│   └── screenshots/
├── models/
├── data/
├── outputs/
└── demo/
    └── demo.mp4
```

## 5. Key Features
*   **Student Features**: Dynamic database filtering, Personalized event recommendations via interest tags, one-click PDF Exports, Google Forms registration links.
*   **Organizer Features**: Automated event creation, OCR extraction fallback to manual entry, AI content generation, "Use Original Poster" preservation, secure event deletion.
*   **UI/UX**: Modern "Celsius Fest" aesthetic with glassmorphism, category color badges, and interactive hover states.

## 6. Local AI Models 
*   **Local LLM**: `llama3.2` running via **Ollama**. Selected for its excellent instruction-following capabilities while remaining feasible for consumer laptops.
*   **Local Image Generation**: **AUTOMATIC1111 (Stable Diffusion 1.5)** running locally. Keeps visual synthesis entirely local without relying on midjourney/DALL-E.
*   **OCR**: `EasyOCR` for local text extraction from images.

## 7. Architecture & Workflow
Our application uses a Streamlit frontend interfacing with a SQLite database. Python modules handle interactions with local AI services (Ollama for text, AUTOMATIC1111 for image generation).

*   [View System Architecture Diagram](docs/architecture_diagram.md)
*   [View Organizer Workflow Diagram](docs/workflow_diagram.md)

*(Note: Replace with `![Architecture](docs/architecture.png)` once exported to PNG)*

## 8. AI Workflow
Upload Poster -> OCR -> Local LLM (Structure Data) -> Local LLM (Generate Content & Image Prompt) -> Local Image Model (Generate Background) -> Pillow (Text Overlay) -> Final Poster.

## 9. Technology Stack
| Component | Technology |
| :--- | :--- |
| Frontend/UI | Streamlit + Custom CSS |
| Backend | Python 3.10+ |
| Database | SQLite3 |
| Local LLM | Ollama (`llama3.2`) |
| Image Generation | AUTOMATIC1111 (Stable Diffusion) |
| OCR | EasyOCR |
| PDF Generation | ReportLab |
| Image Manipulation | Pillow (PIL) |

## 10. Hardware Requirements
*   **Minimum**: CPU-only, 16GB RAM (Ollama will run slower, Image Generation relies on CPU flags `--no-half`).
*   **Recommended**: NVIDIA GPU (6GB+ VRAM) for hardware-accelerated EasyOCR and fast local model inference.

## 11. Screenshots
*(Add your application screenshots here by placing them in the `docs/screenshots/` folder)*
*   ![Dashboard](docs/screenshots/dashboard_placeholder.png)
*   ![Organizer Portal](docs/screenshots/portal_placeholder.png)

## 12. Demo Video
Watch the full AI workflow in action:
*(Upload your video to the demo folder and link it here)*

[🎥 Watch the Demo Video](demo/demo.mp4)

## 13. Installation & Usage
### Setup
```bash
git clone <repo-url>
cd CampusEventPlatform
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Configuration
1. Install [Ollama](https://ollama.com/) locally.
2. Run `ollama run llama3.2` in terminal to download the model.
3. Ensure AUTOMATIC1111 WebUI is running with the `--api` flag (and `--no-half --skip-torch-cuda-test` if on CPU).

### Running the Application
```bash
python -m streamlit run app.py
```

## 14. Privacy
**100% Local.** No student data or event information is sent to OpenAI, Google, or any cloud provider.

## 15. Academic Context
Developed for M.Sc. Data Analytics at CHRIST (Deemed to be University), Bengaluru Central Campus.
