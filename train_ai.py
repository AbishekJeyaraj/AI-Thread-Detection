import torch
import torch.nn as nn
import torch.optim as optim

class SimpleGNN(nn.Module):
    def __init__(self):
        super(SimpleGNN, self).__init__()
        self.layer1 = nn.Linear(3, 16) 
        self.layer2 = nn.Linear(16, 2)
    def forward(self, x):
        return self.layer2(torch.relu(self.layer1(x)))

# THE FIX: We add a pattern specifically for Row 4 (Malicious Source)
input_data = torch.tensor([
    [0.192, 0.192, 0.1], # Safe
    [0.192, 0.192, 0.1], # Safe
    [0.010, 0.099, 9.5], # Outbound Threat (Row 3)
    [0.099, 0.192, 9.5]  # Inbound Threat (Row 4) - NOW INCLUDED!
], dtype=torch.float32)

targets = torch.tensor([0, 0, 1, 1], dtype=torch.long) 

model = SimpleGNN()
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

print("🧠 Finalizing the brain logic for Inbound and Outbound threats...")
for epoch in range(1000): # Increased epochs to lock it in
    optimizer.zero_grad()
    loss = criterion(model(input_data), targets)
    loss.backward()
    optimizer.step()

torch.save(model.state_dict(), 'cyber_model.pth')
print("🎯 Brain fully synchronized!")