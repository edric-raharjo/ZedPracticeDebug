import os

from models.model import train_and_save_model
from utils.preprocess import load_and_split_data
from utils.visualize import save_scatter_plot


def main():
    csv_path = "data/iris.csv"
    graph_dir = "storage/graphs"
    model_dir = "storage/models"

    print("Step 1: Visualizing data...")
    save_scatter_plot(csv_path, graph_dir)

    print("Step 2: Loading and splitting data...")
    X_train, X_test, y_train, y_test = load_and_split_data(csv_path)

    print("Step 3: Training model...")
    model = train_and_save_model(X_train, y_train, model_dir)

    # Score accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy on test set: {accuracy:.2f}")


if __name__ == "__main__":
    main()
