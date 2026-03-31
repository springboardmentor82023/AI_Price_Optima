import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Dummy dataset
X = np.array([
    [100, 50, 0.5],
    [120, 60, 0.6],
    [80, 30, 0.3],
    [150, 80, 0.7],
    [90, 40, 0.4]
])

y = np.array([200, 250, 150, 300, 180])  # demand

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model created successfully!")
