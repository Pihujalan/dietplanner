import pickle
import pandas as pd
import os

def load_model(model_path):
    """Load the trained model"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    print(f"✅ Model loaded successfully from {model_path}")
    print(f"Model type: {type(model)}")
    return model

def predict_calories():
    """Predict calories using the trained model"""
    print("🍎 Calorie Prediction System")
    print("="*40)
    
    # Try to find available model files
    model_files = [
        "../models/calorie_model.pkl",
        "../models/diet_model (2).pkl", 
        "../models/diet_model (1).pkl",
        "../models/trained_model.pkl"
    ]
    
    model = None
    model_path = None
    
    for model_file in model_files:
        if os.path.exists(model_file):
            try:
                model = load_model(model_file)
                model_path = model_file
                break
            except Exception as e:
                print(f"❌ Could not load {model_file}: {str(e)}")
                continue
    
    if model is None:
        print("❌ No working model found. Please check if model files exist.")
        return
    
    # Example new data (make sure same preprocessing as training!)
    new_data = pd.DataFrame([{
        "Weight": 64,
        "Height": 155,  # Note: This seems to be in cm, but our data uses feet
        "Age": 20,
        "Gender": "Male",          # if you used encoding, encode here too
        "Activity level": "Very active"
    }])
    
    print(f"\n📊 Input Data:")
    print(new_data)
    
    try:
        # Prediction
        pred = model.predict(new_data)
        print(f"\n🎯 PREDICTION RESULT:")
        print(f"Predicted value: {pred}")
        
        # If it's a calorie prediction, display it nicely
        if len(pred) > 0:
            if isinstance(pred[0], (int, float)):
                print(f"Predicted Calories: {pred[0]:.0f} kcal/day")
            else:
                print(f"Predicted Category: {pred[0]}")
        
        return pred
        
    except Exception as e:
        print(f"❌ Error during prediction: {str(e)}")
        print("This might be due to feature mismatch or data preprocessing differences.")
        return None

def predict_with_user_input():
    """Interactive prediction with user input"""
    print("\n🍎 Interactive Calorie Prediction")
    print("="*40)
    
    # Try to find available model files
    model_files = [
        "../models/calorie_model.pkl",
        "../models/diet_model (2).pkl", 
        "../models/diet_model (1).pkl",
        "../models/trained_model.pkl"
    ]
    
    model = None
    model_path = None
    
    for model_file in model_files:
        if os.path.exists(model_file):
            try:
                model = load_model(model_file)
                model_path = model_file
                break
            except Exception as e:
                print(f"❌ Could not load {model_file}: {str(e)}")
                continue
    
    if model is None:
        print("❌ No working model found. Please check if model files exist.")
        return
    
    # Get user input
    print("\n📝 Please enter your details:")
    
    try:
        weight = float(input("Weight (kg): "))
        height = float(input("Height (feet, e.g., 5.5): "))
        age = int(input("Age: "))
        gender = input("Gender (Male/Female): ").title()
        activity = input("Activity Level (Sedentary/Lightly Active/Moderately Active/Very Active): ").title()
        
        # Create input data
        new_data = pd.DataFrame([{
            "Weight": weight,
            "Height": height,  # in feet
            "Age": age,
            "Gender": gender,
            "Activity level": activity
        }])
        
        print(f"\n📊 Your Input Data:")
        print(new_data)
        
        # Prediction
        pred = model.predict(new_data)
        print(f"\n🎯 PREDICTION RESULT:")
        print(f"Predicted value: {pred}")
        
        # Display result nicely
        if len(pred) > 0:
            if isinstance(pred[0], (int, float)):
                print(f"Predicted Calories: {pred[0]:.0f} kcal/day")
            else:
                print(f"Predicted Category: {pred[0]}")
        
        return pred
        
    except ValueError:
        print("❌ Invalid input. Please enter numeric values for weight, height, and age.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Choose prediction method:")
    print("1. Use example data (64kg, 155cm, 20yr, Male, Very active)")
    print("2. Enter your own data")
    
    choice = input("\nEnter choice (1/2): ").strip()
    
    if choice == "1":
        predict_calories()
    elif choice == "2":
        predict_with_user_input()
    else:
        print("Invalid choice. Please run again and choose 1 or 2.")
