import os
import torch

from torch.utils.data import Dataset, DataLoader

class DicomContourDataset(Dataset):

    def __init__(self, input_csv_mapping, transofrm=None):
        self.input_csv_mapping = input_csv_mapping
        self.transform = transform

        data = 0
        with open(self.input_csv_mapping, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            next(reader, None)
            for row in reader:
                data += 1

    def __len__(self):
        return self.data

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()


diacomContourDataset = DicomContourDataset(input_dir="")
dataloader = DataLoader(diacomContourDataset, batch_size=8, shuffle=True,
                        num_workers=4)