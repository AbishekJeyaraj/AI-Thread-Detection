import torch
import torch.nn as nn
from datetime import datetime

# 1. Define the Brain Structure
class SimpleGNN(nn.Module):
    def __init__(self):
        super(SimpleGNN, self).__init__()
        self.layer1 = nn.Linear(3, 16)
        self.layer2 = nn.Linear(16, 2)
    def forward(self, x):
        return self.layer2(torch.relu(self.layer1(x)))

# 2. Load the saved knowledge
model = SimpleGNN()
model.load_state_dict(torch.load('cyber_model.pth'))
model.eval()

def log_threat(src, dest, size, status):
    """Writes the detection results to a permanent file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] SRC: {src} | DEST: {dest} | SIZE: {size}MB | STATUS: {status}\n"
    
    with open("threat_log.txt", "a") as f:
        f.write(log_entry)

print("🛡️ Advanced Cyber-Scanner Active (Forensics Enabled)...")

# 3. Ask the user for data
try:
    src = float(input("Enter Source ID: "))
    dest = float(input("Enter Dest ID: "))
    size = float(input("Enter Data Size: "))

    new_data = torch.tensor([[src, dest, size]], dtype=torch.float32)
    prediction = torch.argmax(model(new_data))

    status = "ALERT" if prediction == 1 else "CLEAN"
    
    if status == "ALERT":
        print("🚨 ALERT: High-Risk Connection Detected!")
    else:
        print("✅ CLEAN: Normal Traffic.")
    
    # Save the result to the log file automatically
    log_threat(src, dest, size, status)
    print("📝 Result saved to threat_log.txt")

except Exception as e:
    print(f"Error: {e}")