# 🩺 Tanit Health AI - Technical Report

**Candidate:** Naim Dabbebi
**Role:** Generative AI Intern

## 1. System Architecture
I built a **Microservices Architecture** to ensure modularity and scalability:
- **Orchestrator:** LangGraph (Hierarchical Supervisor-Worker pattern).
- **Database:** Neo4j (Graph for topology + Vector Index for semantic retrieval).
- **Backend:** FastAPI (Exposes agent logic via REST).
- **Frontend:** Streamlit (Provides a chat interface, data visualization, and reporting).

## 2. Agent Workflow (Reasoning)
I implemented a **Supervisor-Worker** architecture:
1.  **Medical Intern (Worker):** Analyzes the user query. It decides whether to fetch medical data (Neo4j) or perform calculations (BMI Tool). It supports **Multi-Context Processing (MCP)** by calling multiple tools in parallel.
2.  **Supervisor (Guardrail):** Intercepts the Intern's draft. It strictly enforces formatting (bold keywords) and ensures a medical disclaimer is present before sending the final response to the user.

## 3. GraphRAG Pipeline
To answer queries like *"I have a fever and headache"*, the system uses a **Hybrid Retrieval** strategy:
1.  **Vector Search:** Embeds the user query (using `all-MiniLM-L6-v2`) to find the top 3 semantically similar Disease nodes.
2.  **Graph Traversal:** Retrieves the specific `(:Symptom)` and `(:Precaution)` nodes connected to those diseases.
3.  **Synthesis:** The LLM combines the unstructured description with the structured graph relationships.

## 4. API Documentation
**Endpoint:** `POST /chat`
**Port:** 8000

**Sample cURL Request:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the symptoms of Malaria?"}'
