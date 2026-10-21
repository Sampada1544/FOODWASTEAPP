import pandas as pd
import joblib
import os


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "food_priority_model.pkl"
)


model = joblib.load(MODEL_PATH)


def predict_priority(
    food_type,
    quantity_kg,
    hours_to_expiry,
    distance_km
):

    data = pd.DataFrame([
        {
            "food_type": food_type,
            "quantity_kg": quantity_kg,
            "hours_to_expiry": hours_to_expiry,
            "distance_km": distance_km
        }
    ])

    prediction = model.predict(data)

    return prediction[0]