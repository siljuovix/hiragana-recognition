import matplotlib.pyplot as plt
import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader
import glob
from PIL import Image
import re
import numpy as np



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


def encode_labels(path):
    name = get_class_name(path)
    encoding = [True if name == c else False for c in class_names]
    return tf.argmax(encoding)


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
        print(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path, class_name = self.data[idx]
        img = np.array(Image.open(img_path))
        class_id = [True if class_name == c else False for c in self.class_names]
        img_tensor = torch.from_numpy(img)
        class_id = torch.tensor([class_id])
        return img_tensor, class_id


data = CustomDataset()
data.__getitem__(0)
