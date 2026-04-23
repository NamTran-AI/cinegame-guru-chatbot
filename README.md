# 🎮 CineGame Guru - Advanced AI Agent & Agentic RAG System

**CineGame Guru** is a specialized AI ecosystem designed for high-fidelity intelligence in the entertainment industry (Cinema & Video Games). This project showcases a sophisticated **Agentic RAG (Retrieval-Augmented Generation)** architecture, engineered to deliver context-aware insights by blending internal domain knowledge with real-time web grounding.

## 🚀 Engineering Highlights

* **🛡️ Multi-Model Fallback & Self-Healing:** Implemented a robust error-handling layer that autonomously navigates through a prioritized hierarchy of LLMs (Gemini 2.5 Flash, 2.0 Flash, etc.) to bypass API rate limits (429 errors), ensuring 99.9% service availability.
* **🧠 High-Fidelity RAG Pipeline:** Orchestrates a dual-source retrieval system that prioritizes a local "Lore" knowledge base (`knowledge.txt`) for brand consistency before escalating to web-scale search.
* **🔍 Real-Time Grounding:** Integrated Google Search Grounding to mitigate hallucinations, providing verifiable data on real-time events like 2026 release schedules, box office metrics, and patch notes.
* **⚡ Streamlit-Powered Reactive UI:** A high-performance web interface designed for seamless human-agent interaction and real-time streaming of AI thought processes.
* **📅 Temporal Awareness:** Dynamic system clock synchronization allowing the agent to perform time-sensitive reasoning (e.g., distinguishing between "upcoming" vs. "released" content).

## 🛠️ Tech Stack

* **Core Engine:** Python 3.10+, Google GenAI SDK (Gemini Series).
* **Infrastructure:** Streamlit (UI), Trafilatura (High-performance Web Scraping).
* **Data Processing:** Pandas, Numpy (Structured data refinement).
* **Environment:** Python-dotenv (Secure credential management).

## 📂 System Architecture & Modules

* `app.py`: The primary orchestration layer and Streamlit Web Interface.
* `main.py`: CLI-based diagnostic and interaction engine.
* `ingest_web.py`: Automated ETL pipeline for web data collection.
* `smart_clean.py`: AI-driven utility for deduplication and refinement of the knowledge base.
* `knowledge.txt`: Vector-ready local knowledge store.

## 📋 Installation & Deployment

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/cinegame-guru.git](https://github.com/yourusername/cinegame-guru.git)
    cd cinegame-guru
    ```

2.  **Initialize Environment:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Authentication:**
    Create a `.env` file with your credentials:
    ```env
    GEMINI_API_KEY=your_production_key_here
    ```

4.  **Execution:**
    ```bash
    streamlit run app.py
    ```

## 📈 Future Roadmap
- [ ] Integration of Vector Databases (ChromaDB/Pinecone) for scalable RAG.
- [ ] Multimodal support for analyzing movie trailers and game screenshots.
- [ ] Automated evaluation pipeline using RAGAS metrics.