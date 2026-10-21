import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib


# Load dataset
data = pd.read_csv("ml/food_priority_data.csv")


# Input features
X = data[
    [
        "food_type",
        "quantity_kg",
        "hours_to_expiry",
        "distance_km"
    ]
]


# Target
y = data["priority"]


# Categorical column
categorical_features = ["food_type"]


# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "food",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Train model
pipeline.fit(X_train, y_train)


# Accuracy
accuracy = pipeline.score(X_test, y_test)

print("Model trained successfully!")
print("Accuracy:", accuracy)


# Save model
joblib.dump(
    pipeline,
    "ml/food_priority_model.pkl"
)

print("Model saved successfully!")