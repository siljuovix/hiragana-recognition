import random
import matplotlib.pyplot as plt
import pandas as pd
import romkan
import numpy as np
import os


def read_class_map():
    keys = pd.read_csv("data_hiragana/kmnist_classmap.csv", sep=",")
    keys["romaji"] = keys["char"].apply(lambda row: romkan.to_roma(row))
    keys = keys.drop(columns=["codepoint", "char"])
    id2label = {k:v for k,v in zip(list(keys["index"]),list(keys["romaji"]))}
    label2id = {v:k for k,v in id2label.items()}
    return id2label, label2id

def plot_random_examples(data):
    plt.figure(figsize=(12,6))
    for i in range(10):
        idx = random.randint(0, len(data))
        image, _ , class_name = data[idx]
        ax=plt.subplot(2,5,i+1)
        ax.title.set_text(class_name)
        plt.imshow(image.squeeze(), cmap="gray")
