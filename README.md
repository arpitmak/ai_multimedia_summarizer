AI Multimedia Note Summarizer (RAG-Based)

An AI-powered backend application that ingests Youtube content (YouTube URL) and enables summarization and question-answering using a Retrieval-Augmented Generation (RAG) pipeline.

Built with FastAPI and focused on practical GenAI system design.

Demo Video-https://drive.google.com/file/d/1WJsIC1LXJP7E8niUk8vv8PmDb22Tzvi0/view?usp=drive_link

Features

Youtube ingestion (YouTube URL)

AI-based transcription

Text chunking & embeddings

Vector-based semantic retrieval

Context-aware Q&A

Automatic summarization

REST APIs with Swagger docs

Tech Stack

Backend: FastAPI (Python)

GenAI: RAG pipeline (embeddings + retrieval)

Vector DB: ChromaDB

Tools: yt-dlp, ffmpeg, pydantic-settings

Run Locally
git clone https://github.com/your-username/ai-multimedia-summarizer.git

cd ai-multimedia-summarizer

python -m venv venv

source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload


Open:

Swagger: http://127.0.0.1:8000/docs

Health: http://127.0.0.1:8000/api/v1/health

What This Project Demonstrates

Practical implementation of RAG systems

Semantic search with vector databases

AI-powered summarization & Q&A

Clean, modular backend architecture

Author

Arpit
AI & Data Science Student | GenAI & RAG Enthusiast
