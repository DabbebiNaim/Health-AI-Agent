import json
import os
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

# --- Configuration ---
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "tanit123")
DATA_FILE = os.path.join("data", "medical_graph_data.json")

# --- Initialize Embedding Model ---
print("⏳ Loading embedding model (this happens once)...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def ingest_data():
    # 1. Connect to Neo4j
    driver = GraphDatabase.driver(URI, auth=AUTH)
    
    with driver.session() as session:
        # 2. Clear existing data (Clean Slate)
        print("🧹 Clearing old database data...")
        session.run("MATCH (n) DETACH DELETE n")
        
        # 3. Create Constraints (Ensures uniqueness and speed)
        print("🔒 Creating constraints...")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Symptom) REQUIRE s.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Precaution) REQUIRE p.name IS UNIQUE")

        # 4. Load JSON
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

        print(f"🚀 Starting ingestion of {len(data)} diseases...")

        for entry in data:
            disease_name = entry['name']
            description = entry['description']
            
            # --- GENERATE EMBEDDING ---
            embedding = model.encode(description).tolist()

            # --- CYPHER QUERY ---
            query = """
            MERGE (d:Disease {name: $name})
            SET d.description = $desc,
                d.embedding = $embedding
            
            WITH d
            UNWIND $symptoms AS sym
            MERGE (s:Symptom {name: sym.name})
            MERGE (d)-[r:HAS_SYMPTOM]->(s)
            SET r.weight = sym.weight

            WITH d
            UNWIND $precautions AS prec
            MERGE (p:Precaution {name: prec})
            MERGE (d)-[:NEEDS_PRECAUTION]->(p)
            """
            
            session.run(query, 
                        name=disease_name, 
                        desc=description, 
                        embedding=embedding,
                        symptoms=entry['symptoms'], 
                        precautions=entry['precautions']
            )
            print(f"   - Imported: {disease_name}")

        # 5. Create Vector Index
        print("🔍 Creating Vector Index for GraphRAG...")
        try:
            # Drop index if it exists
            session.run("DROP INDEX disease_desc_index IF EXISTS")
            
            # Create new index using vector search settings
            session.run("""
            CREATE VECTOR INDEX disease_desc_index IF NOT EXISTS
            FOR (d:Disease) ON (d.embedding)
            OPTIONS {indexConfig: {
             `vector.dimensions`: 384,
             `vector.similarity_function`: 'cosine'
            }}
            """)
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")

    driver.close()
    print("✅ Ingestion Complete! Your Graph is ready.")

if __name__ == "__main__":
    ingest_data()