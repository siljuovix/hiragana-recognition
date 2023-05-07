from torch.utils.data.sampler import SubsetRandomSampler
from torch.utils.data import DataLoader

import torch
import torch.nn as nn
import torch.optim as optim

import numpy as np

from hiragana_recognition import data_loader_torch
from hiragana_recognition import model
from hiragana_recognition import utils

BATCH_SIZE = 8
VALIDATION_SPLIT = .2
SHUFFLE = True
SEED= 42
EPOCHS = 10

def dataset_split(dataset):
    dataset_size = len(data)
    indices = list(range(dataset_size))
    split = int(np.floor(VALIDATION_SPLIT * dataset_size))
    if SHUFFLE :
        np.random.seed(SEED)
        np.random.shuffle(indices)
    train_indices, val_indices = indices[split:], indices[:split]
    train_sampler = SubsetRandomSampler(train_indices)
    valid_sampler = SubsetRandomSampler(val_indices)

    train_loader = torch.utils.data.DataLoader(data, batch_size=BATCH_SIZE, sampler=train_sampler)
    validation_loader = torch.utils.data.DataLoader(data, batch_size=BATCH_SIZE, sampler=valid_sampler)
    return train_loader, validation_loader


def train_cnn(loader_train):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001)

    for epoch in range(EPOCHS):

        running_loss = 0.0
        for i, example in enumerate(loader_train, 0):
            inputs, labels, names = example
            optimizer.zero_grad()
            outputs = net(inputs)
            labels = labels.squeeze()
            loss = criterion(outputs, labels.squeeze())
            loss.backward()
            optimizer.step()
            running_loss += loss.item() # for average loss of mini-batches

            if i % 20 == 19:
                print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 20:.3f}')
                running_loss = 0.0

    print("Finished training")



if __init__==__main__:

    data = data_loader_torch.CustomDataset()

    print("dataset info: ")
    print(f"     Number of characters = {len(data.class_names)}")
    print(f"     Number of examples in the dataset = {len(data)}")

    net = model.Net()
    train, val = dataset_split(data)
    train_cnn(train)
    PATH = './models/model_1.pth'
    torch.save(net.state_dict(), PATH)

    net = Net()
    net.load_state_dict(torch.load(PATH))


    dataiter = iter(val)
    images, labels, c = next(dataiter)
    print(labels) # CREATE BIGGER MODEL

    net.eval()
    outputs = net(images)

    _, predicted = torch.max(outputs, 1)
    predicted
