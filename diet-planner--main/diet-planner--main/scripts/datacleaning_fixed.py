import pandas as pd
import numpy as np
import re

# Load your dataset
df = pd.read_csv("../data/pbl_datasheet.csv")  # change filename if needed

print(f"Original dataset shape: {df.shape}")
print(f"Total rows: {len(df)}")

# Function to clean Food Allergies column
def clean_food_allergies_column(df):
    """
    Clean the Food Allergies column by replacing variations of 'no allergies' with 'Unknown'
    """
    print("\n🧹 Cleaning Food Allergies column...")
    print(f"Food Allergies column unique values before cleaning:")
    print(df['Food Allergies'].value_counts().head(10))
    
    # Define patterns that indicate no allergies
    no_allergy_patterns = [
        r'^no$',                    # "No"
        r'^none$',                  # "None"
        r'^nil$',                   # "Nil"
        r'^na$',                    # "NA"
        r'^n/a$',                   # "N/A"
        r'^nothing$',               # "Nothing"
        r'^nope$',                  # "Nope"
        r'^non$',                   # "Non"
        r'^nill$',                  # "Nill" (misspelling)
        r'^no\.$',                  # "No."
        r'^no allergies$',          # "No Allergies"
        r'^no allergy$',            # "No Allergy"
        r'^not aware$',             # "Not Aware"
        r'^not that i know$',       # "Not That I Know"
        r'^not such$',              # "Not Such"
        r'^not so far$',            # "Not So Far"
        r'^not at all$',            # "Not At All"
        r'^not done allergies test', # "Not Done Allergies Test..."
        r'^no one$',                # "No One"
        r'^no curd and diary products$', # "No Curd And Diary Products"
        r'^none27\s+s$',            # "None27   S" (with extra characters)
        r'^nil known$',             # "Nil Known"
        r'^nil but not very fond',  # "Nil But Not Very Fond..."
        r'^nop$',                   # "Nop"
    ]
    
    # Create a combined regex pattern
    combined_pattern = '|'.join(no_allergy_patterns)
    
    # Apply the cleaning
    def clean_allergy_value(value):
        if pd.isna(value) or value == '':
            return 'Unknown'
        
        # Convert to string and strip whitespace
        value_str = str(value).strip()
        
        # Check if it matches any of the "no allergy" patterns (case insensitive)
        if re.match(combined_pattern, value_str, re.IGNORECASE):
            return 'Unknown'

        return value_str
    
    # Apply the cleaning function
    df['Food Allergies'] = df['Food Allergies'].apply(clean_allergy_value)
    
    print(f"\nAfter cleaning:")
    print(f"Food Allergies column unique values:")
    print(df['Food Allergies'].value_counts().head(10))
    
    # Show some statistics
    unknown_count = (df['Food Allergies'] == 'Unknown').sum()
    total_count = len(df)
    print(f"\nFood Allergies Statistics:")
    print(f"Total records: {total_count}")
    print(f"Records with 'Unknown' allergies: {unknown_count}")
    print(f"Percentage with 'Unknown' allergies: {(unknown_count/total_count)*100:.1f}%")
    
    return df

# Function to remove duplicate rows
def remove_duplicate_rows(df):
    """
    Remove duplicate rows from the dataset
    """
    print("\n🗑️ Removing duplicate rows...")
    
    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicate_count}")
    
    if duplicate_count > 0:
        print(f"Percentage of duplicates: {(duplicate_count/len(df))*100:.2f}%")
        
        # Show some examples of duplicate rows
        print(f"\nFirst few duplicate rows:")
        duplicates = df[df.duplicated(keep=False)]
        print(duplicates.head(10))
        
        # Remove duplicates (keep first occurrence)
        df_cleaned = df.drop_duplicates(keep='first')
        
        print(f"\nAfter removing duplicates:")
        print(f"Cleaned dataset shape: {df_cleaned.shape}")
        print(f"Rows removed: {len(df) - len(df_cleaned)}")
        
        return df_cleaned
    else:
        print("No duplicate rows found in the dataset!")
        return df

# Apply cleaning functions
df = clean_food_allergies_column(df)
df = remove_duplicate_rows(df)

print(f"\n📊 After initial cleaning: {df.shape}")

# ===== VERTEX AI OPTIMIZED CLEANING =====

# Function to handle missing values
def handle_missing_values(df):
    """Handle missing values for Vertex AI compatibility"""
    print("\n🔧 Handling missing values...")
    
    # Check for missing values
    missing_data = df.isnull().sum()
    print("Missing values per column:")
    print(missing_data[missing_data > 0])
    
    # Fill missing values
    # Numeric columns - fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
            print(f"Filled {col} with median: {df[col].median():.2f}")
    
    # Categorical columns - fill with mode or 'Unknown'
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_value = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
            df[col].fillna(mode_value, inplace=True)
            print(f"Filled {col} with mode: {mode_value}")
    
    return df

# Function to standardize categorical variables
def standardize_categorical_variables(df):
    """Standardize all categorical variables for consistency"""
    print("\n🏷️ Standardizing categorical variables...")
    
    # Standardize Gender
    df['Gender'] = df['Gender'].str.title()
    print(f"Gender values: {df['Gender'].unique()}")
    
    # Standardize Activity Level
    activity_mapping = {
        'sedentary': 'Sedentary',
        'lightly active': 'Lightly Active', 
        'moderately active': 'Moderately Active',
        'very active': 'Very Active'
    }
    df['Activity level'] = df['Activity level'].str.title()
    print(f"Activity level values: {df['Activity level'].unique()}")
    
    # Standardize Eating Preference
    eating_mapping = {
        'vegetarian': 'Vegetarian',
        'non vegetarian': 'Non Vegetarian',
        'eggetarian': 'Eggetarian',
        'vegan': 'Vegan'
    }
    df['Eating preference'] = df['Eating preference'].str.title()
    print(f"Eating preference values: {df['Eating preference'].unique()}")
    
    return df

# Function to extract specific food allergen keywords
def extract_allergen_keywords(df):
    """Extract specific individual allergen keywords from long food allergy descriptions"""
    print("\n🥜 Extracting specific allergen keywords...")
    
    # Define specific allergens (matching exact spelling from dataset)
    specific_allergens = [
        # Dairy products
        'milk', 'curd', 'cheese', 'paneer', 'dairy',
        # Grains & Gluten
        'wheat', 'gluten',
        # Proteins
        'meat',
        # Nuts
        'nuts', 'peanuts', 'peanut',
        # Seafood
        'fish', 'prawn', 'shrimp', 'crab', 'lobster', 'seafood',
        # Soy products
        'soya', 'soya chunks',
        # Mushrooms
        'mushroom', 'mushrooms', 'musrooms',  # Note: "musrooms" is misspelled in dataset
        # Vegetables
        'broccoli', 'brocolli',  # Note: "brocolli" is misspelled in dataset
        'cauliflower', 'cabbage', 'cabage',  # Note: "cabage" is misspelled in dataset
        'capsicum', 'onion', 'garlic',
        # Fruits
        'pineapple', 'avocado', 'figs',
        # Pulses
        'besan', 'rajma', 'quinoa', 'oats',
        # Spices & Others
        'sugar',
        # Sprouts
        'sprouts'
    ]
    
    def extract_keywords(text):
        if pd.isna(text) or str(text).lower() in ['unknown', 'no', 'none', 'nil', 'na', 'nothing']:
            return 'Unknown'
        
        text_lower = str(text).lower()
        found_allergens = []
        
        # Check for each specific allergen
        for allergen in specific_allergens:
            if allergen in text_lower:
                found_allergens.append(allergen.title())
        
        if not found_allergens:
            return 'Unknown'

        # Return sorted, unique specific allergens
        return ', '.join(sorted(set(found_allergens)))
    
    # Apply the extraction
    df['Food Allergies'] = df['Food Allergies'].apply(extract_keywords)
    
    # Show statistics
    print("Specific allergens found:")
    allergen_counts = df['Food Allergies'].value_counts()
    print(allergen_counts.head(10))
    
    # Show examples of extracted keywords
    print("\nExamples of extracted specific allergens:")
    examples = df[df['Food Allergies'] != 'Unknown']['Food Allergies'].unique()[:10]
    for example in examples:
        print(f"  - {example}")
    
    return df

# Function to recalculate BMI correctly
def recalculate_bmi(df):
    """Recalculate BMI using correct height and weight values"""
    print("\n📐 Recalculating BMI values...")
    
    # Convert height from feet.decimal to meters
    df['Height_m'] = pd.to_numeric(df['Height'], errors='coerce') * 0.3048
    
    # Ensure weight is in kg
    df['Weight_kg'] = pd.to_numeric(df['Weight_kg'], errors='coerce')
    
    # Recalculate BMI: BMI = weight(kg) / height(m)²
    df['BMI'] = df['Weight_kg'] / (df['Height_m'] ** 2)
    
    # Check for invalid BMI values
    invalid_bmi = df[(df['BMI'] < 10) | (df['BMI'] > 60)]
    if len(invalid_bmi) > 0:
        print(f"Found {len(invalid_bmi)} invalid BMI values (outside 10-60 range)")
        print("Invalid BMI examples:")
        print(invalid_bmi[['Weight_kg', 'Height', 'Height_m', 'BMI']].head())
    
    # Cap BMI values to reasonable range
    df['BMI'] = df['BMI'].clip(lower=10, upper=60)
    
    print(f"BMI range after recalculation: {df['BMI'].min():.2f} - {df['BMI'].max():.2f}")
    print(f"Average BMI: {df['BMI'].mean():.2f}")
    
    return df

# Function to handle outliers
def handle_outliers(df):
    """Handle outliers using IQR method"""
    print("\n📊 Handling outliers...")
    
    numeric_cols = ['Weight_kg', 'Height', 'Age', 'BMI']
    outliers_removed = 0
    
    for col in numeric_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if len(outliers) > 0:
                print(f"Found {len(outliers)} outliers in {col}")
                # Cap outliers instead of removing them
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
                outliers_removed += len(outliers)
    
    print(f"Total outliers handled: {outliers_removed}")
    return df

# Function to create feature engineering
def create_features(df):
    """Create additional features for better model performance"""
    print("\n⚙️ Creating additional features...")
    
    # BMI categories (simplified)
    df['BMI_Detailed'] = pd.cut(df['BMI'], 
                               bins=[0, 18.5, 25, 30, 100],
                               labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    # Weight categories
    df['Weight_Category'] = pd.cut(df['Weight_kg'], 
                                  bins=[0, 50, 65, 80, 100, 200],
                                  labels=['Light', 'Normal', 'Heavy', 'Very_Heavy', 'Extreme'])
    
    # Activity level encoding
    activity_encoding = {'Sedentary': 1, 'Lightly Active': 2, 'Moderately Active': 3, 'Very Active': 4}
    df['Activity_Score'] = df['Activity level'].map(activity_encoding)
    
    print("New features created: BMI_Detailed, Weight_Category, Activity_Score")
    return df

# Function to calculate daily calorie needs (TDEE)
def calculate_calories(df):
    """Calculate daily calorie needs using Mifflin-St Jeor formula"""
    print("\n🔥 Calculating daily calorie needs (TDEE)...")
    
    def calculate_calories_row(row):
        """Helper function to calculate calories for a single row"""
        # Extract values
        weight = row["Weight_kg"]   # kg
        height = row["Height"]      # feet (like 5.2)
        age = row["Age"]
        gender = row["Gender"]
        activity = row["Activity level"]

        # Convert height from feet to cm
        height_cm = height * 30.48

        # Step 1: BMR using Mifflin–St Jeor equation
        if gender.lower() == "male":
            bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161

        # Step 2: Activity multiplier
        activity_multipliers = {
            "Sedentary": 1.2,
            "Lightly Active": 1.375,
            "Moderately Active": 1.55,
            "Very Active": 1.725,
            "Extra Active": 1.9
        }

        multiplier = activity_multipliers.get(activity, 1.2)  # default sedentary
        tdee = bmr * multiplier

        return round(tdee, 2)

    # Apply the calculation to each row
    df["Calories"] = df.apply(calculate_calories_row, axis=1)
    
    print(f"Calorie calculation completed!")
    print(f"Calorie range: {df['Calories'].min():.0f} - {df['Calories'].max():.0f} kcal/day")
    print(f"Average calories: {df['Calories'].mean():.0f} kcal/day")
    
    return df

# Function to finalize dataset (without encoding)
def finalize_dataset(df):
    """Finalize dataset by removing unnecessary columns"""
    print("\n🚀 Finalizing dataset...")
    
    # Remove unnecessary columns
    columns_to_remove = ['Unnamed: 9', 'Height_m']  # Remove redundant columns
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
    
    print(f"Final dataset shape: {df.shape}")
    print(f"Final columns: {list(df.columns)}")
    
    return df

# Apply all cleaning functions
print("\n" + "="*50)
print("🧹 COMPREHENSIVE DATA CLEANING")
print("="*50)

df = handle_missing_values(df)
df = extract_allergen_keywords(df)
df = recalculate_bmi(df)
df = standardize_categorical_variables(df)
df = handle_outliers(df)
df = create_features(df)
df = calculate_calories(df)
df = finalize_dataset(df)

print(f"\n✅ FINAL CLEANED DATASET")
print(f"Shape: {df.shape}")
print(f"Data types: {df.dtypes.value_counts()}")
print(f"No missing values: {df.isnull().sum().sum() == 0}")

# Save the cleaned dataset
print("\n💾 Saving cleaned dataset...")
cleaned_file = "../data/cleaned_dataset.csv"
df.to_csv(cleaned_file, index=False)
print(f"💾 Cleaned dataset saved to: {cleaned_file}")

# Also save as dataset_with_calories.csv as requested
calories_file = "../data/dataset_with_calories.csv"
df.to_csv(calories_file, index=False)
print(f"💾 Dataset with calories saved to: {calories_file}")

# Print first 5 rows to confirm
print("\n📊 First 5 rows of the cleaned dataset:")
print(df.head())

print("\n🎯 Dataset is now clean and ready for use!")
