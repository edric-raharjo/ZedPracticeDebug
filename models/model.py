import os
import pickle

from sklearn.linear_model import LogisticRegression


def train_and_save_model(X_train, y_train, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Initialize and train model
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    # Save trained model as pickle (.pkl)
    model_path = os.path.join(output_dir, "iris_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    return model
