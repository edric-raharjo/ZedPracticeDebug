import os

import matplotlib.pyplot as plt
import pandas as pd


def save_scatter_plot(filepath, output_dir):
    df = pd.read_csv(filepath)
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(6, 4))
    for species, group in df.groupby("species"):
        plt.scatter(group["sepal_length"], group["sepal_width"], label=species)

    plt.xlabel("Sepal Length")
    plt.ylabel("Sepal Width")
    plt.legend()
    plt.title("Iris Sepal Dimensions")
    plt.savefig(os.path.join(output_dir, "iris_scatter.png"))
    plt.close()
