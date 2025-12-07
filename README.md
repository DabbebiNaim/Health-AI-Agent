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
```
### 3. Environment Setup
Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```
Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
Install the required libraries:
```bash
pip install -r requirements.txt
```

### 4. Configuration (.env)
Create a .env file in the root directory and add your credentials:
```ini
# Groq API Key (for the LLM)
GROQ_API_KEY=gsk_your_key_here

# Neo4j Local Database Credentials
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_database_password
```
### 5. Database Ingestion
This script loads the raw CSV data, generates vector embeddings, and populates the Neo4j Graph.
1-Make sure your Neo4j Database is Running.
2-Run the ingestion script:
```bash
python ingest_data.py
```

You should see "✅ Ingestion Complete!"

## 🛠️ Tool Definitions

The agent has access to **two custom tools** defined in `multi_agent.py`:

### 1. `consult_medical_database`
- **Description:** Performs a hybrid search (Vector + Cypher) on the Neo4j Knowledge Graph.
- **Input:** Natural language symptom description (e.g., "headache and fever").
- **Output:** Structured text containing matching diseases, symptoms, and precautions.

### 2. `calculate_bmi`
- **Description:** A utility tool for calculating Body Mass Index.
- **Input:** `weight_kg` (float), `height_m` (float).
- **Output:** The calculated BMI value.
