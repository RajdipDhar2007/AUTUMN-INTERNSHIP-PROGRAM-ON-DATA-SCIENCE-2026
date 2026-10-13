from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Shared volume mounted by Docker Compose
MODEL_PATH = Path("/models/iris_model.joblib")
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

# Load the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# Train and evaluate
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Test accuracy: {accuracy:.3f}")

# Save the model into the shared volume
joblib.dump(model, MODEL_PATH)

print(f"Model saved to {MODEL_PATH}")