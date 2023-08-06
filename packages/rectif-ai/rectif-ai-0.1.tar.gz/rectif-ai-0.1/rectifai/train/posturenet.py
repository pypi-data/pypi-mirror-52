import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from torchsummary import summary

from rectifai.models.posturenet import PostureNetwork
from rectifai.settings import *
from rectifai.models.posturenet.config import *
from rectifai.data.dataset.posturenet import PostureDataset

# Fully connected neural network with two hidden layer
model = PostureNetwork().to(device)
summary(model, (1,input_size))

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  

data_loaders = {mode :  DataLoader(dataset= \
    PostureDataset(mode), batch_size=batch_size,shuffle=True) \
    for mode in ['train','val','test']}

print(len(data_loaders['train'])*batch_size,":",len(data_loaders['val'])*batch_size)

def train():
    for epoch in range(num_epochs):
        for i, (pose_coordinates, labels) in enumerate(data_loaders['train']):  

            # Move tensors to the configured device
            pose_coordinates = pose_coordinates.reshape(-1, input_size).to(device)
            labels = labels.to(device)
            
            # Forward pass
            outputs = model(pose_coordinates)
            loss = criterion(outputs, labels)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()

            #optimize
            optimizer.step()
            
            # show logs
            if (i+1) % 100 == 0:
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, i+1, len(data_loaders['train']), loss.item()))

        # Test the model after each epoch
        with torch.no_grad():
            correct, total = 0, 0
            for pose_coordinates, labels in data_loaders['val']:
                pose_coordinates = pose_coordinates.reshape(-1, input_size).to(device)
                labels = labels.to(device)
                outputs = model(pose_coordinates)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            print('Accuracy of the network on the test dataset: {} %'.format(100 * correct / total))

train()
# Save the model checkpoint
torch.save(model.state_dict(), 'data/raw/posturenet.pth')
