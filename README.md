# 🎮 CineGame Guru - RAG-Powered AI Chatbot

A specialized AI assistant designed to explore and explain Easter Eggs and mysteries in video games (focusing on GTA V). This project implements **RAG (Retrieval-Augmented Generation)** to provide highly accurate, lore-specific information from custom knowledge bases.

## 🚀 Key Features
- **Generative AI Integration**: Powered by **Google Gemini 2.5 Flash** for natural and engaging conversations.
- **RAG Architecture**: Leverages a custom knowledge base (`kienthuc.txt`) to bypass AI hallucinations and provide factual data on specific game mysteries (e.g., The Mount Gordo Ghost, Infinity Killer, Vinewood Orange Ball).
- **Automated Model Validation**: Includes a diagnostic script (`check_models.py`) to verify API capabilities and available models.
- **Secure Configuration**: Implements environment variable management for sensitive API credentials.

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **AI Framework**: `google-genai` (Google's latest Generative AI SDK)
- **Environment Management**: `python-dotenv`
- **Data Handling**: File-based RAG system

## 📋 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/yourusername/cinegame-guru.git](https://github.com/yourusername/cinegame-guru.git)
   cd cinegame-guru