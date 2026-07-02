# SHL Assessment Recommendation Assistant

An AI-powered conversational recommendation system that helps recruiters identify the most suitable SHL assessments based on job roles, required skills, and hiring requirements.

The assistant uses **Retrieval-Augmented Generation (RAG)** by combining semantic search over the SHL assessment catalog with Google's Gemini model to provide accurate, explainable recommendations.

---

# Features

- Semantic search using Sentence Transformers
- FAISS vector database for fast retrieval
- Google Gemini for recommendation generation
- Conversational recommendation support
- Follow-up question handling
- Clarification for vague queries
- SHL catalog restricted responses
- FastAPI REST API
- Swagger API documentation

---

# Architecture

```
                User

                  │

                  ▼

           FastAPI API

                  │

                  ▼

       Conversation Handler

                  │

                  ▼

        Semantic Retriever

        (Sentence Transformer)

                  │

                  ▼

              FAISS

                  │

                  ▼

      Top Matching Assessments

                  │

                  ▼

              Gemini

                  │

                  ▼

      Final Recommendation

                  │

                  ▼

            JSON Response
```

---

# Tech Stack

- Python 3.12
- FastAPI
- FAISS
- Sentence Transformers
- Google Gemini
- Pydantic
- Uvicorn

---

# Folder Structure

```
shl-assessment-agent/

│

├── app/

│   ├── api/

│   ├── core/

│   ├── data/

│   ├── models/

│   ├── services/

│   └── main.py

│

├── scripts/

├── tests/

├── README.md

├── requirements.txt

└── .env.example
```

---

# Installation

Clone repository

```bash
git clone https://github.com/yourusername/shl-assessment-agent.git
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# Run

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# API

## GET /health

Returns server health.

Response

```json
{
  "status":"ok"
}
```

---

## POST /chat

Example Request

```json
{
  "query":"Need Python Backend Developer assessment",
  "conversation_history":[]
}
```

Example Response

```json
{
  "reply":"Recommended assessments...",

  "recommendations":[...],

  "needs_clarification":false,

  "end_of_conversation":false
}
```

---

# Retrieval Pipeline

1. User submits hiring requirement.
2. Query is converted into embeddings.
3. FAISS retrieves the most relevant SHL assessments.
4. Retrieved assessments are passed to Gemini.
5. Gemini generates recommendations.
6. API returns structured JSON.

---

# Future Improvements

- Redis conversation memory
- Hybrid retrieval (BM25 + FAISS)
- Assessment reranking
- Authentication
- User feedback collection
- Deployment monitoring

---

# Author

Harsh Kumar

B.Tech Graduate

Python | AI | Machine Learning | FastAPI