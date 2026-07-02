# SHL Assessment Recommendation Assistant

## Approach Document

**Candidate:** Harsh Kumar

---

# Problem Understanding

The objective of this project is to build an AI-powered assistant capable of recommending appropriate SHL assessments based on natural language hiring requirements.

Instead of requiring recruiters to manually search through hundreds of assessments, the assistant understands the hiring requirement, retrieves relevant assessments from the SHL catalog, and generates recommendations with explanations.

The solution also supports conversational interactions by considering previous conversation history while generating recommendations.

---

# Overall Solution

The system follows a Retrieval-Augmented Generation (RAG) architecture.

Instead of allowing the Large Language Model to answer directly, the assistant first retrieves relevant assessments from the SHL catalog using semantic search.

Only those retrieved assessments are provided to the language model, which significantly reduces hallucinations and keeps recommendations grounded in the official SHL catalog.

The workflow is shown below.

```
User

↓

FastAPI

↓

Conversation Context

↓

Retriever

↓

FAISS

↓

Top Matching Assessments

↓

Gemini

↓

JSON Response
```

---

# Data Preparation

The SHL product catalog was converted into JSON format.

Each assessment contains information such as:

- Assessment Name
- Description
- Duration
- Job Levels
- Categories
- Remote Support
- Adaptive Support
- Assessment URL

These records are transformed into dense vector embeddings.

---

# Semantic Search

Sentence Transformers (`all-MiniLM-L6-v2`) are used to convert every assessment into a vector representation.

A FAISS index stores these vectors for efficient similarity search.

When a recruiter submits a query, the query is also converted into an embedding.

The nearest assessments are retrieved based on semantic similarity rather than keyword matching.

This allows the system to retrieve relevant assessments even when the wording differs from the catalog.

---

# Large Language Model

Google Gemini is responsible for generating recruiter-friendly recommendations.

The retrieved assessments are provided as context together with the recruiter query.

The prompt instructs Gemini to:

- recommend only retrieved assessments
- explain every recommendation
- ask clarification questions when necessary
- avoid generating assessments that are not present in the catalog

This keeps recommendations accurate and interpretable.

---

# Conversation Handling

The assistant accepts previous conversation history.

Instead of processing only the latest query, earlier user messages are considered while retrieving assessments.

For example,

User:

Need Python backend assessments.

Later:

Also include personality.

The assistant combines both requests before generating recommendations.

This produces more relevant multi-turn conversations.

---

# API Design

The project exposes two REST endpoints.

## GET /health

Returns service health.

## POST /chat

Accepts

- user query
- conversation history

Returns

- assistant response
- recommended assessments
- clarification status
- conversation completion flag

FastAPI automatically provides Swagger documentation.

---

# Design Decisions

## Why FastAPI?

FastAPI provides high performance, automatic validation using Pydantic, and interactive API documentation.

---

## Why Sentence Transformers?

Semantic embeddings perform significantly better than keyword matching for natural language hiring requirements.

---

## Why FAISS?

FAISS performs efficient nearest-neighbor search even for large vector collections.

This makes recommendation generation fast and scalable.

---

## Why Gemini?

Gemini generates natural language explanations while remaining grounded by retrieved SHL assessments.

Its role is reasoning rather than searching.

---

# Limitations

Current limitations include:

- conversation memory is supplied by the client instead of persistent storage
- recommendations depend on retrieved catalog quality
- no authentication
- no user feedback loop
- no hybrid retrieval

---

# Future Improvements

Potential future enhancements include:

- Redis conversation memory
- Hybrid Search (BM25 + FAISS)
- Assessment reranking
- User authentication
- Feedback-based learning
- Docker deployment
- CI/CD pipeline
- Monitoring and logging

---

# Conclusion

The proposed solution combines semantic retrieval with a Large Language Model to build an intelligent SHL assessment recommendation assistant.

The system remains grounded in the SHL catalog while providing conversational recommendations that are more accurate than traditional keyword-based search.