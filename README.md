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
3. Environment Setup
Create a virtual environment to isolate dependencies:
Windows:
code
Bash
python -m venv venv
.\venv\Scripts\activate
Mac/Linux:
code
Bash
python3 -m venv venv
source venv/bin/activate
Install the required libraries:
code
Bash
pip install -r requirements.txt
4. Configuration (.env)
Create a .env file in the root directory and add your credentials:
code
Ini
# Groq API Key (for the LLM)
GROQ_API_KEY=gsk_your_key_here

# Neo4j Local Database Credentials
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_database_password
5. Database Ingestion
This script loads the raw CSV data, generates vector embeddings, and populates the Neo4j Graph.
Make sure your Neo4j Database is Running.
Run the ingestion script:
code
Bash
python ingest_data.py
You should see "✅ Ingestion Complete!"
🏃‍♂️ How to Run
The system runs as two separate processes: the Backend API and the Frontend UI.
Step 1: Start the Backend API
Open a terminal and run:
code
Bash
python api.py
The API will start at http://localhost:8000
Step 2: Start the Frontend UI
Open a new terminal (keep the first one running) and run:
code
Bash
streamlit run ui.py
The UI will open automatically in your browser at http://localhost:8501
🧪 Usage Examples
1. Medical Triage (GraphRAG)
Query: "I have a high fever, severe headache, and joint pain."
Behavior: The Intern Agent searches Neo4j using vector similarity. It finds "Dengue" or "Typhoid". The Supervisor formats the advice and adds a chart of confidence scores.
2. Multi-Context Processing (MCP)
Query: "I weigh 100kg and I am 1.8m tall. Also, I have yellow skin."
Behavior: The Agent executes two tools in parallel:
calculate_bmi (Math)
consult_medical_database (Graph Search for "yellow skin")
Result: It returns the BMI calculation AND the medical diagnosis (Jaundice/Hepatitis) in a single answer.
📂 Project Structure
code
Code
├── api.py                  # FastAPI Backend Server
├── ui.py                   # Streamlit Frontend Interface
├── multi_agent.py          # LangGraph Supervisor/Worker Logic
├── graph_tools.py          # Neo4j Retrieval & Vector Search Tools
├── ingest_data.py          # ETL Script (CSV -> Neo4j)
├── clean_data.py           # Data preprocessing script
├── requirements.txt        # Project dependencies
└── data/                   # Dataset files (CSV/JSON)
