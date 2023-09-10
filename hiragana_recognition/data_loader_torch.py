import matplotlib.pyplot as plt
import os
import torch
from torchvision import datasets, transforms

import glob
from PIL import Image
import re
import numpy as np

from hiragana_recognition import model, utils


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, ), (0.5, ))])

def get_class_name(file_loc):
    name = os.path.split(file_loc)[1]
    end = re.search(r"\d+", name).start()
    chars = name[4:end]
    return chars

def get_class_names(data_list):
    class_names = set()
    for loc in data_list:
        lbl = get_class_name(loc)
        class_names.add(lbl)
    return class_names

class CustomDataset(Dataset):
    def __init__(self):
        self.imgs_path = "data/"
        file_list = glob.glob(self.imgs_path + "*")
        self.data = []
        class_names = set()
        for class_path in file_list:
            class_name = get_class_name(class_path)
            class_names.add(class_name)
            for img_path in glob.glob(class_path):
                self.data.append([img_path, class_name])
        self.img_dim = (84, 83)
        self.class_names = list(class_names)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path, class_name = self.data[idx]
        img = np.array(Image.open(img_path))
        img = transform(img)
        class_id = [self.class_names.index(class_name)]
        class_id = torch.tensor([class_id])
        return img, class_id, class_name
