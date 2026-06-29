import pandas as pd
from sklearn.model_selection import train_test_split


def load_and_split_data(filepath):
    # Load dataset
    df = pd.read_csv(filepath)
    X = df.drop(columns=["species"])
    y = df["species"]

    # Split into Train and Test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test
