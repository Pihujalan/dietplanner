import pandas as pd
import numpy as np

def calculate_calories_mifflin_st_jeor(weight, height, age, gender, activity_level):
    """
    Calculate daily calorie needs using Mifflin-St Jeor equation
    
    Parameters:
    - weight: weight in kg
    - height: height in feet (e.g., 5.5)
    - age: age in years
    - gender: "Male" or "Female"
    - activity_level: activity level string
    
    Returns:
    - daily calorie needs in kcal
    """
    # Convert height from feet to cm
    height_cm = height * 30.48
    
    # BMR calculation using Mifflin-St Jeor equation
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
    
    # Activity multipliers
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    
    # Get multiplier, default to sedentary if not found
    multiplier = activity_multipliers.get(activity_level, 1.2)
    
    # Calculate Total Daily Energy Expenditure (TDEE)
    tdee = bmr * multiplier
    
    return round(tdee, 2)

def predict_bmi_category(weight, height):
    """Predict BMI category based on weight and height"""
    # Convert height from feet to meters
    height_m = height * 0.3048
    
    # Calculate BMI
    bmi = weight / (height_m ** 2)
    
    # Determine category
    if bmi < 18.5:
        return "Underweight", bmi
    elif bmi < 25:
        return "Normal", bmi
    elif bmi < 30:
        return "Overweight", bmi
    else:
        return "Obese", bmi

def predict_single_user():
    """Interactive prediction for a single user"""
    print("🍎 Direct Calorie & BMI Prediction System")
    print("="*50)
    
    print("\n📝 Please enter your details:")
    
    try:
        weight = float(input("Weight (kg): "))
        height = float(input("Height (feet, e.g., 5.5): "))
        age = int(input("Age: "))
        gender = input("Gender (Male/Female): ").title()
        activity = input("Activity Level (Sedentary/Lightly Active/Moderately Active/Very Active): ").title()
        
        # Calculate predictions
        calories = calculate_calories_mifflin_st_jeor(weight, height, age, gender, activity)
        bmi_category, bmi_value = predict_bmi_category(weight, height)
        
        # Display results
        print(f"\n🎯 PREDICTION RESULTS:")
        print(f"Calculated BMI: {bmi_value:.2f}")
        print(f"BMI Category: {bmi_category}")
        print(f"Daily Calorie Needs: {calories:.0f} kcal")
        
        # Health insights
        print(f"\n💡 HEALTH INSIGHTS:")
        if bmi_value < 18.5:
            print("• Consider consulting a nutritionist for healthy weight gain")
            print("• Focus on nutrient-dense foods and strength training")
        elif bmi_value < 25:
            print("• Great! You're in the healthy weight range")
            print("• Maintain your current lifestyle and eating habits")
        elif bmi_value < 30:
            print("• Consider moderate weight loss through diet and exercise")
            print("• Aim for a calorie deficit of 500-750 kcal per day")
        else:
            print("• Consider consulting a healthcare provider for weight management")
            print("• Focus on sustainable lifestyle changes")
        
        # Activity recommendations
        print(f"\n🏃 ACTIVITY RECOMMENDATIONS:")
        if activity == "Sedentary":
            print("• Try to increase daily movement")
            print("• Start with 10-15 minutes of walking daily")
        elif activity == "Lightly Active":
            print("• Good start! Try to increase intensity")
            print("• Add 2-3 strength training sessions per week")
        elif activity == "Moderately Active":
            print("• Excellent! You're on the right track")
            print("• Consider adding variety to your workouts")
        else:
            print("• Outstanding! Keep up the great work")
            print("• Remember to include rest days for recovery")
        
        return {
            'weight': weight,
            'height': height,
            'age': age,
            'gender': gender,
            'activity_level': activity,
            'bmi': bmi_value,
            'bmi_category': bmi_category,
            'daily_calories': calories
        }
        
    except ValueError:
        print("❌ Invalid input. Please enter numeric values for weight, height, and age.")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def predict_batch_data():
    """Predict for the cleaned dataset"""
    print("\n🍎 Batch Prediction for Cleaned Dataset")
    print("="*50)
    
    try:
        # Load the cleaned dataset
        df = pd.read_csv("../data/cleaned_dataset.csv")
        print(f"✅ Loaded {len(df)} records from cleaned dataset")
        
        # Calculate predictions for all records
        predictions = []
        
        for index, row in df.iterrows():
            # Use existing data
            weight = row['Weight_kg'] if 'Weight_kg' in row else row['Weight']
            height = row['Height']
            age = row['Age']
            gender = row['Gender']
            activity = row['Activity level']
            
            # Calculate predictions
            calories = calculate_calories_mifflin_st_jeor(weight, height, age, gender, activity)
            bmi_category, bmi_value = predict_bmi_category(weight, height)
            
            predictions.append({
                'index': index,
                'bmi': bmi_value,
                'bmi_category': bmi_category,
                'daily_calories': calories
            })
        
        # Create predictions DataFrame
        pred_df = pd.DataFrame(predictions)
        
        # Merge with original data
        result_df = df.copy()
        result_df['Predicted_BMI'] = pred_df['bmi']
        result_df['Predicted_BMI_Category'] = pred_df['bmi_category']
        result_df['Predicted_Daily_Calories'] = pred_df['daily_calories']
        
        # Save results
        output_file = "../data/direct_predictions.csv"
        result_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Batch predictions completed!")
        print(f"Results saved to: {output_file}")
        
        # Show statistics
        print(f"\n📊 PREDICTION STATISTICS:")
        print(f"BMI Category Distribution:")
        print(result_df['Predicted_BMI_Category'].value_counts())
        
        print(f"\nCalorie Range: {result_df['Predicted_Daily_Calories'].min():.0f} - {result_df['Predicted_Daily_Calories'].max():.0f} kcal")
        print(f"Average Calories: {result_df['Predicted_Daily_Calories'].mean():.0f} kcal")
        
        # Show sample results
        print(f"\n📋 Sample Results:")
        sample_cols = ['Weight', 'Height', 'Age', 'Gender', 'Predicted_BMI', 'Predicted_BMI_Category', 'Predicted_Daily_Calories']
        print(result_df[sample_cols].head(10).to_string(index=False))
        
        return result_df
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def predict_example_data():
    """Predict using the example data from your original code"""
    print("\n🍎 Example Data Prediction")
    print("="*50)
    
    # Your original example data
    weight = 64
    height = 155 / 30.48  # Convert cm to feet (155cm = ~5.08 feet)
    age = 20
    gender = "Male"
    activity = "Very active"
    
    print(f"Example Data:")
    print(f"  Weight: {weight} kg")
    print(f"  Height: {height:.2f} feet (155 cm)")
    print(f"  Age: {age} years")
    print(f"  Gender: {gender}")
    print(f"  Activity: {activity}")
    
    # Calculate predictions
    calories = calculate_calories_mifflin_st_jeor(weight, height, age, gender, activity)
    bmi_category, bmi_value = predict_bmi_category(weight, height)
    
    print(f"\n🎯 PREDICTION RESULTS:")
    print(f"Calculated BMI: {bmi_value:.2f}")
    print(f"BMI Category: {bmi_category}")
    print(f"Daily Calorie Needs: {calories:.0f} kcal")
    
    return {
        'weight': weight,
        'height': height,
        'age': age,
        'gender': gender,
        'activity_level': activity,
        'bmi': bmi_value,
        'bmi_category': bmi_category,
        'daily_calories': calories
    }

if __name__ == "__main__":
    print("🍎 Direct Prediction System")
    print("Choose prediction method:")
    print("1. Use example data (64kg, 155cm, 20yr, Male, Very active)")
    print("2. Enter your own data")
    print("3. Batch prediction for cleaned dataset")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        predict_example_data()
    elif choice == "2":
        predict_single_user()
    elif choice == "3":
        predict_batch_data()
    else:
        print("Invalid choice. Please run again and choose 1, 2, or 3.")
