from neo4j import GraphDatabase
import pandas as pd
import os

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "riddimagenius0958"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# -------- CREATE OUTPUT FOLDER --------
OUTPUT_DIR = "exported_graph"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------- FETCH EDGES --------
def get_edges(tx):
    query = """
    MATCH (a)-[r]->(b)
    RETURN id(a) AS src, id(b) AS dst, type(r) AS rel
    """
    return list(tx.run(query))

# -------- FETCH NODES --------
def get_nodes(tx):
    query = """
    MATCH (n)
    RETURN id(n) AS neo4j_id, labels(n)[0] AS type
    """
    return list(tx.run(query))

with driver.session() as session:
    edges = session.execute_read(get_edges)
    nodes = session.execute_read(get_nodes)

edges_df = pd.DataFrame([dict(r) for r in edges])
nodes_df = pd.DataFrame([dict(r) for r in nodes])

# -------- SAVE FILES IN FOLDER --------
edges_path = os.path.join(OUTPUT_DIR, "edges.csv")
nodes_path = os.path.join(OUTPUT_DIR, "nodes.csv")

edges_df.to_csv(edges_path, index=False)
nodes_df.to_csv(nodes_path, index=False)

print(f"✅ Files saved in folder: {OUTPUT_DIR}")