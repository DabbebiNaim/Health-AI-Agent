# 🩺 Tanit Health AI - Agentic GraphRAG System

> **Generative AI Internship Submission**  
> **Candidate:** Naim Dabbebi

## 📋 Overview
Tanit Health AI is a **Multi-Agent Medical Assistant** designed to provide clinical advice by reasoning over a **Neo4j Knowledge Graph**. 

Unlike standard chatbots, this system uses a **Hierarchical Agent Architecture** (Supervisor-Worker pattern) to ensure accuracy, safety, and structured output. It features a **Hybrid GraphRAG** pipeline that combines vector similarity search with graph traversal to retrieve symptoms, precautions, and disease descriptions.

## ✨ Key Features
- **🧠 Multi-Agent Orchestration:** Powered by **LangGraph**. An "Intern" agent retrieves data, while a "Supervisor" agent validates the response and enforces safety protocols.
- **🕸️ GraphRAG:** Uses **Neo4j** for structured retrieval and **Vector Embeddings** (`all-MiniLM-L6-v2`) for semantic search.
- **⚡ Multi-Context Processing (MCP):** The agent can perform mathematical calculations (BMI) and medical retrieval in parallel within a single reasoning step.
- **📊 Analytics UI:** A **Streamlit** frontend that visualizes the "Chain of Thought" reasoning process and plots diagnostic confidence scores.
- **🔌 Microservices:** Decoupled architecture with a **FastAPI** backend and **Streamlit** frontend.

---

## 🛠️ Tech Stack
- **LLM:** Llama-3.3-70b (via Groq)
- **Orchestration:** LangGraph, LangChain
- **Database:** Neo4j (Graph + Vector Store)
- **Backend:** FastAPI, Pydantic
- **Frontend:** Streamlit, Altair
- **ETL:** Pandas, Sentence-Transformers

---

## 🚀 Setup & Installation

Follow these steps to run the project locally.

### 1. Prerequisites
- Python 3.9+
- **Neo4j Desktop** (Installed and active)
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/DabbebiNaim/Health-AI-Agent.git
cd Health-AI-Agent
