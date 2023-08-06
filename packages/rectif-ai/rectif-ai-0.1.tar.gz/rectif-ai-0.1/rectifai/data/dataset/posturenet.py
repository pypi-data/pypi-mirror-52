import torch 
from torch.utils.data import Dataset

class PostureDataset(Dataset):
    def __init__(self, mode):
        self.x = torch.load(f'data/processed/X_{mode}.pt')
        self.y = torch.load(f'data/processed/y_{mode}.pt')
        

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]