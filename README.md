# Semantic Cache Proxy for LLMs

## Overview

The **Semantic Cache Proxy** is a high-performance, intelligent middleware acting as a bridge between your application and Large Language Model (LLM) APIs.

Traditional caching mechanisms rely on exact string matching, which is highly ineffective for conversational AI where users frequently ask the exact same question in slightly different ways (e.g., "What's the capital of France?" vs "Can you tell me the French capital?").

This proxy solves this by caching responses based on **semantic similarity**. It calculates vector embeddings of incoming prompts and serves cached responses for "like" or semantically identical queries without ever hitting the upstream LLM provider.

## 🎯 Key Benefits

- **Massive Cost Savings**: By intercepting repetitive or semantically similar queries, you significantly reduce the number of tokens sent to expensive LLM providers (like OpenAI, Anthropic, etc.).
- **Reduced Latency**: Computing an embedding and performing a vector search in Redis takes mere milliseconds—drastically faster than waiting for an LLM to generate a response from scratch.
- **Rate-Limit Protection**: Shields your upstream LLM APIs from traffic spikes and aggressive rate limiting.

## 🏗️ What Was Built in This Project

This project implements a robust, Dockerized FastAPI application equipped with the following core components:

- **FastAPI Backend (`app/main.py`)**: A lightweight, async REST API to receive prompts.
- **Embeddings Engine (`app/services/embeddings.py`)**: Converts incoming text prompts into vector representations using a fast, local, or lightweight embedding model.
- **Vector Database (`app/db/redis.py`)**: Utilizes Redis (via Docker) as a blazing-fast vector database to store prompt embeddings and their corresponding LLM outputs.
- **Semantic Cache Logic (`app/services/cache.py`)**: Performs cosine similarity searches on incoming prompts against the Redis vector store. If the similarity score exceeds a defined threshold, it registers a **Cache Hit**.
- **LLM Fallback (`app/services/llm.py`)**: If a semantic match is not found (a **Cache Miss**), the proxy forwards the request to the upstream LLM, returns the response to the user, and asynchronously caches the new prompt/response pair for future use.
- **Metrics & Monitoring (`app/services/metrics.py`)**: Tracks cache hit/miss ratios, latency improvements, and estimated cost savings.

## 🚀 Real-World Applications

Proper implementation of a semantic cache unlocks powerful capabilities for various production applications:

1.  **Customer Support Chatbots**: Users constantly ask variations of "How do I reset my password?" or "Where is my order?". Semantic caching absorbs this repetitive volume instantly for free.
2.  **Enterprise RAG Systems**: In Retrieval-Augmented Generation, users often query internal company documents looking for the same operational guidelines.
3.  **Educational Apps & Tutors**: Serving high-traffic platforms where students might be asking similar questions about a specific curriculum or syllabus.
4.  **Development & Automated Testing**: When actively developing LLM features, developers run the same test suites repeatedly. Semantic caching prevents burning API credits during local development.

## 🛠️ Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Your preferred LLM API keys

### Installation & Setup

1. **Spin up the Vector Database (Redis):**

   ```bash
   docker compose up -d redis
   ```

2. **Install dependencies:**
   Ensure your virtual environment is activated, then run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Set up your environment variables (e.g., `OPENAI_API_KEY`, Redis connection strings) in your `.env` file (refer to `.env.example`).

4. **Run the Proxy:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📈 Future Enhancements

- Implementing cache eviction policies (e.g., TTL based on vector age or access frequency).
- Dynamic similarity thresholds based on query complexity.
- Support for caching inputs and the responses.
