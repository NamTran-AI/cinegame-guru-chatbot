# 🎮 CineGame Guru - Advanced AI Agent & RAG System

CineGame Guru is a specialized AI assistant designed for the entertainment industry (Cinema, Video Games, Comics). This project implements an **Agentic RAG (Retrieval-Augmented Generation)** architecture, combining custom knowledge bases with real-time web intelligence.

## 🚀 Key Features

- **🤖 AI-Powered RAG**: Utilizes **Gemini 2.5 Flash** to retrieve and process information from a custom knowledge base (`knowledge.txt`), providing lore-specific accuracy.
- **🌐 Web Knowledge Ingestor**: Automated scripts to crawl and extract clean content from authoritative URLs (Wikipedia, IGN, Fandom, etc.), building your AI's "brain" in seconds.
- **🧹 Smart Cleanup (AI-Driven)**: Automatically analyzes and purifies raw data. It filters out system "noise" (error codes, ads) and merges duplicate entries to optimize internal knowledge.
- **🔍 Real-time Grounding**: Integrated **Google Search** capabilities. Guru can provide up-to-date information for 2026 (movie schedules, latest trailers) beyond the limits of static training data.
- **🎭 Professional Persona**: Engages in smart, witty, and lore-heavy conversations using gaming and cinema enthusiast terminology.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **AI Engine**: `google-genai` (Gemini 2.0 Flash & 2.5 Flash Experimental)
- **Data Scraping**: `trafilatura`
- **Configuration**: `python-dotenv` (Secure API management)
- **Architecture**: Agentic RAG with Google Search Grounding tools.

## 📂 Project Structure

- `main.py`: The core Chatbot integrated with Google Search and RAG.
- `ingest_web.py`: Automated web data collection script.
- `smart_clean.py`: AI tool for refining and deduplicating the knowledge base.
- `knowledge.txt`: The processed "Internal Brain" containing specialized data.

## 📋 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/yourusername/cinegame-guru.git](https://github.com/yourusername/cinegame-guru.git)
   cd cinegame-guru