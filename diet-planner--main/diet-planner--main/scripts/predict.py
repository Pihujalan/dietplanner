from pycaret.regression import load_model, predict_model
import pandas as pd

# Load the model
model = load_model("../models/diet_model (2)")

# Example new data
new_data = pd.DataFrame([{
    "Weight": 65,
    "Height": 5.6,
    "Age": 29,
    "Gender": "Female",
    "Activity level": "Sedentary"
}])

# Make prediction
pred = predict_model(model, data=new_data)
print(pred)
