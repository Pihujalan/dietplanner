import pickle
import pandas as pd

# Load model
with open("", "rb") as f:
    model = pickle.load(f)

# Example new data (make sure same preprocessing as training!)
new_data = pd.DataFrame([{
    "Weight": 64,
    "Height": 155,
    "Age": 20,
    "Gender": "Male",          # if you used encoding, encode here too
    "Activity level": "Very active"
}])

# Prediction
pred = model.predict(new_data)
print(pred)
