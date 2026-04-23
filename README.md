# 🎮 CineGame Guru - Advanced AI Agent & RAG System

**CineGame Guru** is a specialized AI assistant designed for the entertainment industry (Cinema, Video Games). This project implements a sophisticated **Agentic RAG (Retrieval-Augmented Generation)** architecture, combining custom internal lore with real-time web intelligence.

## 🚀 Key Features

* **🌐 Streamlit Web UI:** A clean, modern chat interface for a seamless user experience.
* **🧠 Context-Aware Memory:** Maintains full conversation history, ensuring that subsequent queries inherit relevant context (e.g., keeping specific graphics requirements across multiple questions).
* **🛡️ Smart Fallback & Auto-Retry:** Intelligent error handling that automatically switches between models (Gemini 2.5 Flash, 2.0 Flash, 1.5 Flash) and retries requests to bypass API rate limits.
* **📅 Dynamic Real-Time Timeline:** Automatically synchronizes with the system clock to ensure the AI is always aware of the current date for accurate release status checking.
* **🔍 Google Search Grounding:** Real-time web verification to provide the latest information on trailers, box office results, and patch notes.
* **📚 Specialized RAG:** Prioritizes local data from `knowledge.txt` to maintain lore consistency before checking external sources.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** Streamlit
* **AI Engine:** Google GenAI SDK (Gemini Series)
* **Search Integration:** Google Search Grounding
* **Data Tools:** Trafilatura, Python-dotenv

## 📂 Project Structure

* `app.py`: The main entry point for the Streamlit Web Application.
* `ingest_web.py`: Script for automated web data collection.
* `smart_clean.py`: AI-powered utility for refining and deduplicating the knowledge base.
* `knowledge.txt`: The processed "Internal Brain" containing domain-specific data.

## 📋 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/cinegame-guru.git](https://github.com/yourusername/cinegame-guru.git)
    cd cinegame-guru
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    Create a `.env` file and add your credentials:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

4.  **Launch the application:**
    ```bash
    streamlit run app.py
    ```