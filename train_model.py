import numpy as np
import joblib
from sklearn.linear_model import LinearRegression

# Sample data for training: replace this with your actual training data
X_train = np.array([
    [10, 200, 5, 1, 150, 7, 4, 3, 2, 5],  # Each array is [distance, energy, food, flights, water, waste, household, dairy, fish, plant_based]
    [15, 250, 6, 0, 120, 5, 3, 1, 3, 4],
    [8, 180, 4, 2, 100, 6, 2, 2, 1, 6]
])
y_train = np.array([300, 400, 280])  # Carbon footprint values for each row in X_train

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'carbon_footprint_model.pkl')
print("Model trained and saved as carbon_footprint_model.pkl")
