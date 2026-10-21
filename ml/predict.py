import pandas as pd
import joblib


# Load trained model
model = joblib.load("ml/food_priority_model.pkl")


# New food donation
new_food = pd.DataFrame([
    {
        "food_type": "Cooked Food",
        "quantity_kg": 5,
        "hours_to_expiry": 4,
        "distance_km": 2
    }
])


# Make prediction
prediction = model.predict(new_food)


print("Food Donation Priority:", prediction[0])