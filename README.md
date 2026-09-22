# 🤖 Production Resume RAG

> An AI-powered Resume Question Answering system built using Retrieval-Augmented Generation (RAG), Hybrid Search, Cross-Encoder Re-ranking, FastAPI and React.

---

## 🚀 Overview

Production Resume RAG is an intelligent resume assistant that allows users to ask natural-language questions about a candidate's resume.

Instead of sending the entire resume directly to an LLM, the system retrieves the most relevant information from the resume and provides it as context to the language model.

The system combines:

- Semantic Search
- BM25 Keyword Search
- Reciprocal Rank Fusion
- Cross-Encoder Re-ranking
- Relevance Filtering
- Contextual Query Understanding
- LLM-based Answer Generation
- Conversation History
- Source Tracking

The goal is to build a practical, production-oriented RAG application rather than a basic PDF chatbot.

---

## ✨ Features

### 🔎 Hybrid Retrieval

Combines two retrieval strategies:

- Semantic Search using embeddings
- BM25 keyword search

This allows the system to understand both semantic meaning and exact keyword matches.

---

### 🧠 Reciprocal Rank Fusion

Results from semantic and keyword retrieval are combined using Reciprocal Rank Fusion (RRF).

```text
Semantic Search
       +
BM25 Keyword Search
       ↓
Reciprocal Rank Fusion
       ↓
Combined Candidates
```

---

### 🎯 Cross-Encoder Re-ranking

The retrieved candidates are passed through a Cross-Encoder model to improve ranking quality.

```text
Hybrid Retrieval
       ↓
Candidate Documents
       ↓
Cross-Encoder
       ↓
Re-ranked Documents
```

---

### 🛡️ Relevance Filtering

The system checks whether retrieved documents are sufficiently relevant before sending them to the LLM.

If the information is not sufficiently relevant, the system avoids generating an unsupported answer.

---

### 💬 Conversational RAG

The application supports multi-turn conversations.

For example:

```text
User:
What technologies does Yukesh know?

AI:
Yukesh knows Java, Python, JavaScript and ReactJS.

User:
What about React?

AI:
Yukesh has experience with ReactJS...
```

Conversation history is used to contextualize follow-up questions.

---

### 📚 Source Tracking

The API returns the retrieved source chunks together with the generated answer.

Example:

```json
{
  "answer": "Yukesh has experience with ReactJS.",
  "sources": [
    {
      "source": "resume.pdf",
      "chunk_index": 2
    }
  ]
}
```

---

### 🌐 Full-Stack Architecture

The project contains:

```text
React
   ↓
FastAPI
   ↓
RAG Pipeline
   ↓
Hybrid Retrieval
   ↓
Re-ranking
   ↓
LLM
```

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │                      │
                         │  Chat Interface      │
                         │  Suggestions         │
                         │  Source Display      │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │                      │
                         │  /chat               │
                         │  /health             │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     ResumeRAG        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │ Query Contextualization    │
                     └──────────────┬─────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │     Hybrid Retrieval       │
                     │                            │
                     │  Semantic Search + BM25    │
                     └──────────────┬─────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │ Reciprocal Rank Fusion     │
                     └──────────────┬─────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │ Cross-Encoder Re-ranking   │
                     └──────────────┬─────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │    Relevance Filtering     │
                     └──────────────┬─────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │      Context Builder       │
                     └──────────────┬─────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │        LLM / Groq          │
                     └──────────────┬─────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Answer + Sources     │
                         └──────────────────────┘
```

---

# 🧩 RAG Pipeline

The complete pipeline is:

```text
PDF Resume
    ↓
PDF Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
ChromaDB
    ↓
User Question
    ↓
Query Embedding
    ↓
Semantic Search
    +
BM25 Search
    ↓
RRF
    ↓
Cross-Encoder Re-ranking
    ↓
Relevance Check
    ↓
Context Building
    ↓
Prompt Construction
    ↓
LLM
    ↓
Answer
    +
Sources
```

---

# 🛠️ Tech Stack

## Frontend

- React
- Vite
- JavaScript
- CSS
- Fetch API

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## AI / RAG

- Sentence Transformers
- `all-MiniLM-L6-v2`
- Cross-Encoder
- BM25
- ChromaDB
- Reciprocal Rank Fusion
- Groq LLM API

## Development

- Git
- GitHub
- VS Code
- Python Virtual Environment

---

# 📁 Project Structure

```text
Production-Resume-RAG/
│
├── backend/
│   │
│   ├── app.py
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   │
│   ├── data/
│   │   └── resume.pdf
│   │
│   ├── chroma_db/
│   │
│   └── src/
│       ├── __init__.py
│       ├── config.py
│       ├── loaders.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── ingest.py
│       ├── corpus.py
│       ├── semantic_search.py
│       ├── keyword_search.py
│       ├── hybrid_search.py
│       ├── rrf.py
│       ├── reranker.py
│       ├── advanced_retriever.py
│       ├── prompts.py
│       ├── llm.py
│       ├── context_builder.py
│       ├── relevance.py
│       ├── source_builder.py
│       ├── query_contextualizer.py
│       └── rag.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── tests/
│   └── test_rag.py
│
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Production-Resume-RAG.git
```

```bash
cd Production-Resume-RAG
```

---

# 🐍 Backend Setup

Go to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
backend/.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key

MODEL_NAME=openai/gpt-oss-20b

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

CANDIDATE_K=5

FINAL_K=3
```

Never commit `.env` to GitHub.

---

# 📄 Add Resume

Place your resume PDF here:

```text
backend/data/resume.pdf
```

The PDF is intentionally excluded from Git using `.gitignore`.

---

# 🧠 Build the Vector Database

From:

```text
backend/
```

run:

```powershell
python -m src.ingest
```

Expected process:

```text
Loading PDF...
Loaded XXXX characters.

Chunking...
Created X chunks.

Generating embeddings...
Embedding dimension: 384

Storing in ChromaDB...
Stored X documents.
```

---

# 🚀 Start FastAPI

From:

```text
backend/
```

run:

```powershell
python -m uvicorn app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

# ⚛️ Frontend Setup

Open another terminal.

Go to:

```powershell
cd E:\learn\Production-Resume-RAG\frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🧪 Testing

The RAG pipeline can be tested using:

```powershell
cd E:\learn\Production-Resume-RAG
```

```powershell
python -m tests.test_rag
```

The test covers:

- Technology questions
- Project questions
- Education questions
- Out-of-context questions
- Conversation history
- Follow-up questions

---

# 💬 Example Questions

```text
What technologies does Yukesh know?

What projects has Yukesh worked on?

What is Yukesh's educational background?

What is Yukesh's experience with React?

What about React?

Does Yukesh know ChromaDB?

What is Yukesh's favorite food?
```

The system should answer only using information available in the resume.

---

# 🔍 Retrieval Strategy

This project uses a two-stage retrieval architecture.

## Stage 1 — Candidate Retrieval

Two independent retrieval systems are used:

```text
                User Query
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
   Semantic Search        BM25 Search
          │                   │
          └─────────┬─────────┘
                    ↓
                  RRF
                    ↓
            Candidate Chunks
```

## Stage 2 — Re-ranking

```text
Candidate Chunks
       ↓
Cross-Encoder
       ↓
Relevance Scores
       ↓
Top Documents
```

This improves retrieval quality before context is sent to the LLM.

---

# 🧠 Conversational Query Contextualization

Follow-up questions can depend on previous messages.

For example:

```text
User:
What technologies does Yukesh know?

Assistant:
Yukesh knows Java, Python, JavaScript and ReactJS.

User:
What about React?
```

The system uses the conversation history to understand what "React" refers to before performing retrieval.

---

# 🔒 Security

The project follows several basic security practices:

- API keys stored in environment variables
- `.env` excluded from Git
- Personal resume PDF excluded from Git
- Request length validation
- Conversation message validation
- Controlled CORS origins
- API error handling

---

# 📈 Future Improvements

Planned improvements include:

- [ ] RAG evaluation framework
- [ ] Retrieval precision / recall evaluation
- [ ] Answer quality evaluation
- [ ] Better relevance threshold calibration
- [ ] Logging
- [ ] Authentication
- [ ] Rate limiting
- [ ] Streaming responses
- [ ] Docker deployment
- [ ] Cloud deployment
- [ ] Production monitoring
- [ ] Guardrails
- [ ] Prompt versioning
- [ ] Caching

---

# 🎯 Learning Goals

This project demonstrates practical understanding of:

- Retrieval-Augmented Generation
- Embeddings
- Vector databases
- Semantic search
- Keyword search
- Hybrid retrieval
- Reciprocal Rank Fusion
- Cross-encoder re-ranking
- Contextual retrieval
- Prompt engineering
- LLM integration
- FastAPI
- React
- API integration
- Environment configuration
- Production-oriented RAG architecture

---

# 👨‍💻 Author

**Yukesh G**

React Frontend Developer → AI Engineer

B.E. Computer Science & Engineering

---

## ⭐ Project

If this project helped you understand production RAG systems, consider giving the repository a star.