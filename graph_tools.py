import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

# 1. Load Environment Variables from .env
load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

# Check if credentials exist
if not URI or not AUTH[0] or not AUTH[1]:
    raise ValueError("❌ Error: Neo4j credentials missing in .env file")

# 2. Load Embedding Model 
print("⏳ Loading embedding model in graph_tools...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_medical_context(user_query: str):
    """
    This function performs the Hybrid Search (Vector + Graph):
    1. Converts user query to numbers (embedding).
    2. Finds the most similar 'Disease' node in Neo4j.
    3. Retrieves connected 'Symptoms' and 'Precautions'.
    """
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        
        query_embedding = model.encode(user_query).tolist()
        
        # --- THE CYPHER QUERY ---
        cypher_query = """
        CALL db.index.vector.queryNodes('disease_desc_index', 3, $embedding)
        YIELD node AS d, score
        
        OPTIONAL MATCH (d)-[:HAS_SYMPTOM]->(s:Symptom)
        OPTIONAL MATCH (d)-[:NEEDS_PRECAUTION]->(p:Precaution)
        
        RETURN d.name AS disease,
               d.description AS description,
               score,
               COLLECT(DISTINCT s.name) AS symptoms,
               COLLECT(DISTINCT p.name) AS precautions
        """
        
        results_text = ""
        
        with driver.session() as session:
            result = session.run(cypher_query, embedding=query_embedding)
            
            # Format the database results into plain text for the LLM
            for record in result:
                results_text += f"\n### Disease Found: {record['disease']} (Similarity: {record['score']:.2f})\n"
                results_text += f"**Description:** {record['description']}\n"
                results_text += f"**Symptoms:** {', '.join(record['symptoms'])}\n"
                results_text += f"**Precautions:** {', '.join(record['precautions'])}\n"
                results_text += "-" * 20 + "\n"
                
        driver.close()
        
        if not results_text:
            return "I searched the database, but found no relevant medical records."
            
        return results_text

    except Exception as e:
        return f"Error querying database: {str(e)}"

# --- Test Block (Only runs if you run this file directly) ---
if __name__ == "__main__":
    test_query = "I have a skin rash and itching"
    print(f"\n🩺 Testing Query: '{test_query}'\n")
    response = get_medical_context(test_query)
    print(response)