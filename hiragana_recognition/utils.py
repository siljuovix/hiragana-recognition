import random
import matplotlib.pyplot as plt


def plot_random_examples(data):
    plt.figure(figsize=(12,6))
    for i in range(10):
        idx = random.randint(0, len(data))
        image, _ , class_name = data[idx]
        ax=plt.subplot(2,5,i+1)
        ax.title.set_text(class_name)
        plt.imshow(image.squeeze(), cmap="gray")
