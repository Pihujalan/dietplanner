import pandas as pd
import numpy as np

# Load your dataset
df = pd.read_csv("../data/pbl_datasheet.csv")  # change filename if needed
for col in df.columns:
    print(f"\n🔹 {col} unique values:")
    print(df[col].unique())   # shows actual values
    print(f"Total unique: {df[col].nunique()}")
# 1️⃣ Standardize Height (convert feet.decimal to meters)
df['Height_m'] = pd.to_numeric(df['Height'], errors='coerce') * 0.3048

# 2️⃣ Standardize Weight
df['Weight_kg'] = pd.to_numeric(df['Weight'], errors='coerce')

# 3️⃣ Recalculate BMI safely
df['BMI'] = df['Weight_kg'] / (df['Height_m'] ** 2)

# 4️⃣ Clean Categories

# CATEGORY standardization
df['CATEGORY'] = df['CATEGORY'].replace({
    'Underweight*': 'Underweight',
    'Normal Weight': 'Normal',
    'Obesity': 'Obese',
    'Error': 'Unknown'
})


# ...existing code...

def standardize_medical_issues(text):
    if pd.isna(text) or text.lower() in ['unknown', 'na', 'nil', 'no', '-', 'nothing', 'none', 
                                        'no issues', 'no issue', 'no medical issues', 
                                        'no medical issue', 'no health issues',
                                        'basically no issue', "don't have", "no any",
                                        'see above', 'mentioned above', 'mentioned under health issues']:
        return 'Unknown'

    # Convert to lowercase and remove special characters
    text = str(text).lower().replace('/',' ').replace(',',' ')
    
    # Define conditions and their keywords
    conditions = {
        'PCOS/PCOD': ['pcos', 'pcod'],
        'Thyroid': ['thyroid', 'hypothyroid', 'hashimoto'],
        'Diabetes': ['diabetes', 'diabetic', 'sugar', 'pre-diabetic', 'prediabetic'],
        'Blood Pressure': ['bp', 'blood pressure', 'hypertension'],
        'Fatty Liver': ['fatty liver', 'liver'],
        'Inflammation': ['inflammation', 'inflammatory'],
        'Vitamin Deficiency': ['vitamin', 'deficiency', 'low vitamin', 'low vit'],
        'Cholesterol': ['cholesterol', 'triglycerides', 'hdl', 'ldl'],
        'Hormonal Issues': ['hormonal', 'hormone', 'irregular periods', 'periods'],
        'Weight Issues': ['weight gain', 'obesity', 'overweight', 'weight loss'],
        'Mental Health': ['stress', 'anxiety', 'depression', 'insomnia'],
        'Pain': ['pain', 'ache', 'arthritis', 'joint pain'],
        'Digestive Issues': ['bloating', 'gas', 'constipation', 'ibs', 'acid reflux', 'acidity', 'gastric'],
        'Post Partum': ['post partum', 'postpartum', 'after delivery', 'after baby'],
        'Autoimmune': ['autoimmune', 'immune'],
        'Anemia': ['hemoglobin', 'iron deficiency', 'low iron'],
        'Migraine': ['migraine', 'headache'],
        'Skin Issues': ['acne', 'psoriasis', 'eczema', 'skin'],
    }

    # Find matching conditions
    found_conditions = set()
    
    for condition, keywords in conditions.items():
        if any(keyword in text for keyword in keywords):
            found_conditions.add(condition)
    
    if not found_conditions:
        return 'Unknown'
        
    return ', '.join(sorted(found_conditions))

# Apply standardization to Medical Issue column
df['Medical_Issue_Standardized'] = df['Medical Issue'].apply(standardize_medical_issues)

# Remove the original Medical Issue column if you want (optional)
# df = df.drop('Medical Issue', axis=1)

def standardize_food_allergies(text):
    if pd.isna(text) or text.lower() in ['unknown', 'na', 'nil', 'no', '-', 'nothing', 'none', 
                                        'no allergies', 'not known', 'not aware', 'don\'t know',
                                        'not that i know', 'no food allergies', 'no any',
                                        'not sure', 'non', 'nope', 'nothing as such',
                                        'not known of any', 'no allergies as such']:
        return 'Unknown'

    # Convert to lowercase and remove special characters
    text = str(text).lower().replace('/',' ').replace(',',' ').replace('\n',' ')
    
    # Define allergens and their keywords
    allergens = {
        'Dairy/Lactose': ['milk', 'lactose', 'dairy', 'curd', 'cheese', 'paneer', 'yogurt', 'dahi'],
        'Gluten': ['gluten', 'wheat', 'roti', 'maida'],
        'Eggs': ['egg'],
        'Nuts': ['nuts', 'peanut', 'cashew', 'almond', 'groundnut'],
        'Seafood': ['seafood', 'fish', 'prawn', 'shellfish', 'shrimp'],
        'Soy': ['soy', 'soya', 'tofu'],
        'Mushrooms': ['mushroom', 'mashroom'],
        'Vegetables': ['brinjal', 'capsicum', 'cabbage', 'cauliflower', 'bhindi', 'karela'],
        'Fruits': ['citrus', 'pineapple', 'papaya', 'banana', 'kiwi', 'avocado'],
        'Pulses': ['besan', 'dal', 'chana', 'rajma', 'lentil'],
        'Spices': ['ginger', 'garlic', 'cinnamon', 'mustard']
    }

    # Find matching allergens
    found_allergens = set()
    
    for allergen, keywords in allergens.items():
        if any(keyword in text for keyword in keywords):
            found_allergens.add(allergen)
            
    # Check for dietary preferences (not allergies)
    if any(pref in text for pref in ['vegetarian', 'vegan', 'non-veg']):
        return 'None (Dietary Preference)'
    
    if not found_allergens:
        return 'Other'
        
    return ', '.join(sorted(found_allergens))

# Apply standardization to Food Allergies column
df['Food_Allergies_Standardized'] = df['Food Allergies'].apply(standardize_food_allergies)

# Print unique standardized values to verify
print("\nStandardized Food Allergies:")
print(df['Food_Allergies_Standardized'].unique())
print(f"Total unique standardized categories: {df['Food_Allergies_Standardized'].nunique()}")



# 5️⃣ Handle missing / Unknowns
categorical_cols = ['Food Allergies', 'Medical Issue']
for col in categorical_cols:
    df[col] = df[col].fillna('Unknown')



# 8️⃣ Categorize BMI
def bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

df['BMI_Category'] = df['BMI'].apply(bmi_category)

# 9️⃣ Final type checks
numeric_cols = ['Weight_kg', 'Height_m', 'Age', 'BMI']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

for col in df.columns:
    print(f"\n🔹 {col} unique values:")
    print(df[col].unique())   # shows actual values
    print(f"Total unique: {df[col].nunique()}")

# 1️⃣0️⃣ Save cleaned dataset
df.to_csv("cleaned_dataset_final.csv", index=False)

print("✅ Dataset fully cleaned and saved as cleaned_dataset_final.csv")
