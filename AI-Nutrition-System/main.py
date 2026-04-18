import pandas as pd

# Load dataset
data = pd.read_csv("diet_data.csv")

# User Input
age = int(input("Enter Age: "))
gender = input("Enter Gender (male/female): ").lower()
height = float(input("Enter Height (cm): "))
weight = float(input("Enter Weight (kg): "))
activity = input("Activity level (low/medium/high): ").lower()
goal = input("Goal (loss/gain/maintain): ").lower()
disease = input("Disease (none/diabetes/bp/obesity/hormonal): ").lower()

# BMI
height_m = height / 100
bmi = weight / (height_m ** 2)

# BMR
if gender == "male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# Activity factor
activity_factor = {"low":1.2, "medium":1.55, "high":1.9}
calories = bmr * activity_factor.get(activity, 1.2)

# Age group (UPDATED)
if age <= 19:
    age_group = "Teen"
elif age <= 50:
    age_group = "Adult"
else:
    age_group = "Old"

# BMI condition
if bmi < 18.5:
    diet_type = "Weight Gain"
elif bmi <= 24.9:
    diet_type = "Balanced"
else:
    diet_type = "Weight Loss"

# Goal adjustment
if goal == "loss":
    calories -= 500
elif goal == "gain":
    calories += 500

# Disease rules
rules = []
if disease == "diabetes":
    rules.append("Low Sugar")
elif disease == "bp":
    rules.append("Low Salt")
elif disease == "obesity":
    rules.append("Low Calorie")
elif disease == "hormonal":
    rules.append("High Protein, No Junk")

# Age adjustment
if age_group == "Teen":
    rules.append("High Energy & Protein")
elif age_group == "Old":
    rules.append("Soft, Low Salt, Low Sugar")

# Meal Plan
def get_meal(goal):
    if goal == "loss":
        return {
            "Breakfast": "Oats + Fruits",
            "Lunch": "Chapati + Dal + Salad",
            "Dinner": "Soup + Salad"
        }
    elif goal == "gain":
        return {
            "Breakfast": "Milk + Banana + Peanut Butter",
            "Lunch": "Rice + Dal + Paneer",
            "Dinner": "Chapati + Curd"
        }
    else:
        return {
            "Breakfast": "Poha + Fruits",
            "Lunch": "Chapati + Dal",
            "Dinner": "Light Dinner"
        }

meal_plan = get_meal(goal)

# Output
print("\n===== RESULT =====")
print(f"BMI: {round(bmi,2)}")
print(f"Calories: {round(calories)} kcal")
print(f"Age Group: {age_group}")
print(f"Diet Type: {diet_type}")
print("Special Rules:", ", ".join(rules))

print("\n--- Meal Plan ---")
for meal, food in meal_plan.items():
    print(f"{meal}: {food}")