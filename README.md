🩺 Tanit Health AI – Agentic GraphRAG System

Generative AI Internship Submission
Candidate: Naim Dabbebi

📋 Overview

Tanit Health AI is a Multi-Agent Medical Assistant designed to provide clinical advice by reasoning over a Neo4j Knowledge Graph.

Unlike standard chatbots, this system uses a Hierarchical Agent Architecture (Supervisor → Intern pattern) to ensure accuracy, safety, and structured output.
It features a Hybrid GraphRAG pipeline that combines vector similarity search with graph traversal to retrieve symptoms, precautions, and disease descriptions.

✨ Key Features
🧠 Multi-Agent Orchestration

Powered by LangGraph

Intern Agent → Retrieves medical information from Neo4j

Supervisor Agent → Validates responses, ensures safety, enforces structured output

🕸️ Hybrid GraphRAG

Uses Neo4j for graph traversal

Uses MiniLM-L6-v2 embeddings for semantic vector search

⚡ Multi-Context Processing (MCP)

The agent can perform multiple tools in parallel, such as:

BMI calculations

Medical Graph retrieval

📊 Interactive Analytics UI

A Streamlit dashboard that visualizes:

Chain-of-Thought reasoning traces

Diagnostic confidence bar charts

🔌 Microservices Architecture

FastAPI backend

Streamlit frontend

Neo4j database + embeddings pipeline

🛠️ Tech Stack
Component	Technology
LLM	Llama-3.3-70b (via Groq)
Orchestration	LangGraph, LangChain
Database	Neo4j (Graph DB + Vector Store)
Backend	FastAPI, Pydantic
Frontend	Streamlit, Altair
ETL / Embeddings	Pandas, Sentence-Transformers
🚀 Setup & Installation

Follow these steps to run the system locally.

1. Prerequisites

Python 3.9+

Neo4j Desktop (running and active)

Git

2. Clone the Repository
git clone https://github.com/DabbebiNaim/Health-AI-Agent.git
cd Health-AI-Agent

3. Environment Setup
Windows
python -m venv venv
.\venv\Scripts\activate

Mac/Linux
python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt

4. Configuration (.env)

Create a file named .env and include:

# Groq API Key (for the LLM)
GROQ_API_KEY=gsk_your_key_here

# Neo4j Local Database Credentials
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_database_password

5. Database Ingestion

Make sure Neo4j is running.

Run the ETL script:

python ingest_data.py


You should see:

✔️ Ingestion Complete!

🏃‍♂️ How to Run the System

The system uses two separate processes.

Step 1 — Start the Backend API
python api.py


The API runs at:

➡️ http://localhost:8000

Step 2 — Start the Frontend UI

Open a new terminal (keep API running):

streamlit run ui.py


The UI loads at:

➡️ http://localhost:8501

🧪 Usage Examples
1. Medical Triage (GraphRAG)

Query:

“I have a high fever, severe headache, and joint pain.”

Behavior:

Intern Agent performs vector similarity search in Neo4j

Retrieves likely diseases (e.g., Dengue, Typhoid)

Supervisor reformats the advice + confidence chart

2. Multi-Context Processing (MCP)

Query:

“I weigh 100kg and I am 1.8m tall. Also, I have yellow skin.”

Behavior:
Two tools run in parallel:

calculate_bmi

consult_medical_database

Output includes:

BMI result

Medical match for “yellow skin” (e.g., Jaundice, Hepatitis)

📂 Project Structure
.
├── api.py               # FastAPI Backend Server
├── ui.py                # Streamlit Frontend Interface
├── multi_agent.py       # LangGraph Supervisor/Worker Logic
├── graph_tools.py       # Neo4j Retrieval & Vector Search Tools
├── ingest_data.py       # ETL Script (CSV → Neo4j)
├── clean_data.py        # Data Preprocessing Script
├── requirements.txt     # Project Dependencies
└── data/                # Datasets (CSV, JSON)
