import pandas as pd
import networkx as nx
import matplotlib
# THIS LINE PREVENTS THE POP-UP
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# 1. Load the scanned data
csv_path = 'scan_report.csv'
try:
    df = pd.read_csv(csv_path)
    # Ensure column names match our auto_detect output
    df.columns = df.columns.str.strip().str.lower()
except:
    print("❌ Error: Run auto_detect.py first to create the report!"); exit()

# 2. Build the Graph
G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='ai_decision')

# 3. Design the Map
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5) # k adjusts spacing

# Draw Nodes
nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightgray', edgecolors='black')

# Draw Edges with Color Logic
for u, v, d in G.edges(data=True):
    # Use 'in' to catch '🚫 BLOCKED' or '🚨 THREAT'
    edge_color = 'red' if 'BLOCK' in str(d['ai_decision']) else 'green'
    nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color=edge_color, width=2.5)

nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

plt.title("AI SECURITY TOPOLOGY: REAL-TIME THREAT MAP")

# 4. SAVE AND EXIT
save_path = 'network_map.png'
plt.savefig(save_path, dpi=300) # dpi=300 makes it high quality for printing
plt.close() # This closes the internal plot so it doesn't pop up

print("="*50)
print(f"🖼️  GRAPH SAVED: network_map.png")
print("🚀 CMD is ready for your next command!")
print("="*50)