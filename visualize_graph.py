import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from pyvis.network import Network
import networkx as nx

# 1. Load Credentials
load_dotenv()
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

def generate_interactive_graph():
    print("⏳ Fetching data from Neo4j...")
    driver = GraphDatabase.driver(URI, auth=AUTH)
    
    # Limit to 100 relationships to keep the visual clean and fast
    # You can increase the LIMIT if you want to see the whole monster
    query = """
    MATCH (source)-[r]->(target)
    RETURN labels(source)[0] as source_type, source.name as source_name,
           type(r) as relationship,
           labels(target)[0] as target_type, target.name as target_name
    LIMIT 300
    """
    
    # Initialize a NetworkX graph (PyVis uses this internally)
    G = nx.DiGraph()
    
    with driver.session() as session:
        result = session.run(query)
        
        for record in result:
            src_name = record['source_name']
            src_type = record['source_type']
            tgt_name = record['target_name']
            tgt_type = record['target_type']
            rel_type = record['relationship']
            
            # Add Source Node with Color
            color_map = {
                "Disease": "#ff5733",    # Red/Orange
                "Symptom": "#33ff57",    # Green
                "Precaution": "#3357ff"  # Blue
            }
            
            # Add nodes
            G.add_node(src_name, label=src_name, title=src_type, color=color_map.get(src_type, "gray"))
            G.add_node(tgt_name, label=tgt_name, title=tgt_type, color=color_map.get(tgt_type, "gray"))
            
            # Add edge
            G.add_edge(src_name, tgt_name, title=rel_type)

    driver.close()
    print(f"✅ Data fetched. Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

    # 2. Visualize with PyVis
    print("🎨 Generating HTML visualization...")
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
    
    # Convert NetworkX graph to PyVis
    net.from_nx(G)
    
    # Add physics controls (makes it interactive and fun to drag)
    net.show_buttons(filter_=['physics'])
    
    # Save to file
    output_file = "graph_visualization.html"
    net.save_graph(output_file)
    print(f"🚀 Graph saved to '{output_file}'. Open it in your browser!")

if __name__ == "__main__":
    generate_interactive_graph()