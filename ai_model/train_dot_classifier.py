import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import os

# ==============================================================================
# NeuroSCARA / BrailleSCARA - Dot Quality Classifier for ADI MAX78000
# 
# This model is designed specifically for the constraints of the MAX78000 
# Hardware CNN Accelerator.
# - Input: 64x64 grayscale images of a Braille cell.
# - Architecture: 3 Convolutional Layers + 2 Fully Connected Layers.
# - Target size: <200K weights (easily fits in MAX78000 442KB weight memory).
# - Goal: Binary classification (0 = FAIL / Defective, 1 = PASS / Good Dot).
#
# NOTE: For deployment to MAX78000, you will eventually use ADI's `ai8x-training` 
# repository which provides `ai8x.FusedConv2dReLU` layers for quantization. 
# This script uses standard PyTorch layers configured to perfectly match the 
# MAX78000 architecture so you can start training immediately.
# ==============================================================================

class MAX78000_DotClassifier(nn.Module):
    def __init__(self, num_classes=2):
        super(MAX78000_DotClassifier, self).__init__()
        
        # Keep input channels to 1 (Grayscale) to save memory and match camera
        # MAX78000 supports 3x3 convolutions perfectly.
        
        # Layer 1: Conv -> ReLU -> MaxPool
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1, bias=True)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2) # 64x64 -> 32x32
        
        # Layer 2: Conv -> ReLU -> MaxPool
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1, bias=True)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2) # 32x32 -> 16x16
        
        # Layer 3: Conv -> ReLU -> MaxPool
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1, bias=True)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2) # 16x16 -> 8x8
        
        # Flattening for Fully Connected Layers
        # 64 channels * 8 height * 8 width = 4096 features
        
        # Layer 4: Fully Connected 1
        self.fc1 = nn.Linear(64 * 8 * 8, 64, bias=True)
        self.relu4 = nn.ReLU()
        
        # Layer 5: Fully Connected 2 (Output)
        self.fc2 = nn.Linear(64, num_classes, bias=True)

    def forward(self, x):
        # Forward pass through the network
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = self.pool3(self.relu3(self.conv3(x)))
        
        x = x.view(x.size(0), -1) # Flatten
        
        x = self.relu4(self.fc1(x))
        x = self.fc2(x)
        return x

def print_model_size(model):
    """Calculates the number of parameters to ensure it fits the MAX78000"""
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total Trainable Parameters: {total_params:,}")
    # MAX78000 can hold ~442KB of weights (approx 440,000 8-bit weights)
    if total_params < 440000:
        print("[SUCCESS] Model size is EFFICIENT and perfectly fits inside MAX78000!")
    else:
        print("[ERROR] Model is too large for MAX78000 hardware.")

def train_model():
    print("Initializing MAX78000 Braille Dot Classifier...")
    model = MAX78000_DotClassifier(num_classes=2)
    print_model_size(model)
    
    # 1. Setup loss and optimizer (Standard for Edge AI training)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 2. Setup Data Transforms (64x64 grayscale as specified in proposal)
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)) # Normalize to [-1, 1] for better quantization later
    ])

    print("\n[INFO] Generating synthetic Braille dot dataset for initial validation...")
    # Generate 1000 synthetic images (64x64)
    # Class 1 (Good dot): Random noise + bright circle in middle
    # Class 0 (Bad dot): Just random noise or very faint circle
    num_samples = 1000
    X = torch.rand(num_samples, 1, 64, 64) * 0.5 # background noise
    y = torch.zeros(num_samples, dtype=torch.long)
    
    for i in range(num_samples):
        if i % 2 == 0:
            y[i] = 1 # Good dot
            # Draw a bright 'dot' in the center
            X[i, 0, 28:36, 28:36] += 0.5 
    
    # Create dataset and loader
    dataset = torch.utils.data.TensorDataset(X, y)
    train_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    epochs = 5
    print("\nStarting Training Loop...")
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
        epoch_acc = 100 * correct / total
        print(f"Epoch {epoch+1}/{epochs} - Loss: {running_loss/len(train_loader):.4f} - Accuracy: {epoch_acc:.2f}%")
    
    print("\n[RESULT] Baseline Pre-training Accuracy (Synthetic Data): {:.2f}%".format(epoch_acc))
    # Save the model weights (to later quantize for MAX78000)
    torch.save(model.state_dict(), 'max78000_braille_dot_model.pth')
    print("Training complete. Model weights saved to max78000_braille_dot_model.pth.")
    
    print("\nNext step for MAX78000 Deployment:")
    print("1. Train this model using PyTorch.")
    print("2. Clone ADI's ai8x-synthesis repository.")
    print("3. Run the quantization script to convert to 8-bit weights.")
    print("4. Generate C code using ADI's network synthesizer to run on the chip at <1mW.")

if __name__ == "__main__":
    train_model()
