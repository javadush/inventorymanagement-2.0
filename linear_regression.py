# linear_regression.py

from sklearn.linear_model import LinearRegression
import numpy as np

def perform_linear_regression(data):
    X = np.array([float(entry[0]) for entry in data]).reshape(-1, 1)
    y = np.array([float(entry[1]) for entry in data])

    model = LinearRegression()
    model.fit(X, y)

    return model

