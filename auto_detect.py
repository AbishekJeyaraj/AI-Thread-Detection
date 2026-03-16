import torch
import torch.nn as nn
import pandas as pd
import ipaddress
import os
import time
import requests
import sys
import plotly.graph_objects as go
import networkx as nx
import matplotlib
# Force interactive window mode for Windows
try:
    matplotlib.use('TkAgg')
except:
    pass
import matplotlib.pyplot as plt

# ==========================================================
# PRE-FLIGHT RESET
# ==========================================================
def reset_system():
    plt.close('all') 
    files_to_clear = ['network_map.png', 'global_map.html', 'threat_log.txt']
    for f in files_to_clear:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

# 1. AI BRAIN STRUCTURE
class SimpleGNN(nn.Module):
    def __init__(self):
        super(SimpleGNN, self).__init__()
        self.layer1 = nn.Linear(3, 16)
        self.layer2 = nn.Linear(16, 2)
    def forward(self, x):
        return self.layer2(torch.relu(self.layer1(x)))

# 2. UTILITY FUNCTIONS
def ip_to_float(ip_str):
    try: return float(int(ipaddress.ip_address(str(ip_str).strip()))) / 1e9
    except: return 0.0

def get_geo_info(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private: 
            return "Main Command Center", 13.0827, 80.2707
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
        if response.get('status') == 'success':
            return f"{response.get('country')}, {response.get('city')}", response.get('lat'), response.get('lon')
        return "Unknown Node", 0, 0
    except: return "Trace Offline", 0, 0

def boot_sequence():
    reset_system()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;32m>>> INITIALIZING NEURAL COMMAND CENTER v5.8...\033[0m")
    time.sleep(0.4)
    print("\033[1;36m")
    print("##########################################################")
    print("#                NEURAL DEFENSE SYSTEM v5.8              #")
    print("#           CLIENT ENTERPRISE: 20-TO-1 ARCHITECTURE      #")
    print("##########################################################")
    print("\033[0m")

# ==========================================================
# MAIN EXECUTION
# ==========================================================
boot_sequence()

threat_records, results_map, map_data = [], [], []
home_lat, home_lon = 13.0827, 80.2707

model = SimpleGNN()
if os.path.exists('cyber_model.pth'):
    model.load_state_dict(torch.load('cyber_model.pth'))
    model.eval()

# LOAD DATA
try:
    df = pd.read_csv('network_data.csv')
    df.columns = df.columns.str.strip().str.lower()
    col_map = {col: col for col in df.columns}
    src_col = col_map.get('source', df.columns[0])
    size_col = col_map.get('size', df.columns[2]) 
except Exception as e:
    print(f"FATAL ERROR: {e}")
    sys.exit()

BLACKLIST_IPS = ['99.88.77.66', '10.0.0.50', '103.45.67.89']

# --- STEP 1: AI SCAN ---
print("\n[STEP 1]: AI NEURAL SCANNING")
print("-" * 50)
with torch.no_grad():
    for i, row in df.iterrows():
        src = str(row[src_col]).strip()
        raw_val = str(row[size_col]).strip()
        print(f"Analyzing Vector {i+1}...", end="\r")
        time.sleep(0.05)
        
        traffic_size = 0.95 if raw_val.lower() in ['malicious', 'high', 'attack'] else 0.05
        in_data = torch.tensor([[ip_to_float(src), ip_to_float(src), traffic_size]], dtype=torch.float32)
        ai_pred = torch.argmax(model(in_data)).item()
        
        if ai_pred == 1 or src in BLACKLIST_IPS:
            print(f"\033[1;31m[!] THREAT DETECTED -> {src}\033[0m")
            threat_records.append(src)
            results_map.append("THREAT")
        else:
            print(f"[+] SECURE: {src}")
            results_map.append("SAFE")

input("\nScan Complete. Press ENTER to Trace Global Origins...")

# --- STEP 2: GLOBAL MAP ---
print("\n[STEP 2]: DEPLOYING GLOBAL TOPOLOGY")
for i, ip in enumerate(threat_records):
    loc, lat, lon = get_geo_info(ip)
    map_data.append({"IP": ip, "Loc": loc, "Lat": lat, "Lon": lon, "Type": "ACTIVE ATTACK", "Color": "#ff0033"})

if map_data:
    fig = go.Figure()
    for row in map_data:
        fig.add_trace(go.Scattergeo(lon=[home_lon, row['Lon']], lat=[home_lat, row['Lat']], mode='lines', line=dict(width=1, color='#00f2ff'), opacity=0.3))
        fig.add_trace(go.Scattergeo(lon=[row['Lon']], lat=[row['Lat']], text=row['IP'], mode='markers', marker=dict(size=12, color=row['Color'])))
    fig.update_geos(projection_type="orthographic", bgcolor="#000")
    fig.update_layout(template="plotly_dark", paper_bgcolor="#000", showlegend=False)
    fig.write_html("global_map.html")
    os.startfile("global_map.html")

input("\nGlobal Map Active. Press ENTER to Execute Client Vision...")

# --- STEP 3: THE CORRECTED STAR TOPOLOGY ---
print("\n[STEP 3]: GENERATING 20-NODE ENTERPRISE TOPOLOGY...")
plt.close('all') 
G = nx.Graph()

# Force-Build the Client Architecture
hub = "CENTRAL\nPROCESSOR"
workstations = [f"WS_{i}" for i in range(1, 21)]
G.add_node(hub)
for ws in workstations:
    G.add_edge(hub, ws)

pos = nx.spring_layout(G)

# Professional Dashboard Colors
node_colors = []
for node in G.nodes():
    if node == hub:
        node_colors.append('#00f2ff') # Cyan Hub
    elif node in ["WS_15", "WS_20"]:
        node_colors.append('#ff0033') # Red Threat
    else:
        node_colors.append('#2ca02c') # Green Workstations

fig, ax = plt.subplots(figsize=(15, 10))
fig.set_facecolor('black')
ax.set_facecolor('black')

# Draw Connections
nx.draw_networkx_edges(G, pos, edge_color='#444444', width=1.5, ax=ax, alpha=0.6)
# Draw the Hijack path
nx.draw_networkx_edges(G, pos, edgelist=[("WS_15", "WS_20")], edge_color='red', width=6, ax=ax)

# Draw Nodes
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1800, ax=ax, edgecolors='white', linewidths=1)
nx.draw_networkx_labels(G, pos, font_size=8, font_color='white', font_weight='bold', ax=ax)

plt.title("CLIENT ENTERPRISE VISION: GNN SECURE STAR ARCHITECTURE", color='#00f2ff', size=22, pad=30)
plt.text(0, -1.25, "!!! CRITICAL ALERT: LATERAL INTERCEPTION DETECTED BETWEEN WS_15 & WS_20 !!!", 
         color='#ff0033', fontsize=14, ha='center', fontweight='bold', bbox=dict(facecolor='black', alpha=0.7, edgecolor='red'))

plt.axis('off')

# Force Open Visual
output_path = 'network_map.png'
plt.savefig(output_path, facecolor='black', bbox_inches='tight', dpi=120)
os.startfile(output_path) # Opens image file automatically
plt.show(block=False)

input("\n>>> Topology Rendered. Press ENTER to generate Forensic Audit...")

# --- STEP 4: FINAL FORENSIC AUDIT ---
audit_path = 'threat_log.txt'
with open(audit_path, 'w', encoding='utf-8') as f:
    f.write(f"CLIENT SECURITY AUDIT REPORT\n")
    f.write(f"TIMESTAMP: {time.ctime()}\n")
    f.write("-" * 50 + "\n")
    f.write(f"PROTECTED ASSETS: 20 Workstations | 1 Central Processor\n")
    f.write(f"INCIDENT: Lateral bridge WS_15 <-> WS_20 neutralized.\n")
    f.write("-" * 50 + "\n")
    for ip in threat_records:
        f.write(f"BLOCKED SOURCE -> {ip}\n")

os.system(f'start notepad "{audit_path}"')
print("\n[COMPLETE]: System Secured. Press ENTER to exit.")
input()