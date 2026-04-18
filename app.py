from flask import Flask, render_template, request

app = Flask(__name__)

def calculate(data):
    age = int(data["age"])
    weight = float(data["weight"])
    height = float(data["height"])
    gender = data["gender"]
    activity = data["activity"]
    goal = data["goal"]
    disease = data["disease"]

    height_m = height / 100
    bmi = weight / (height_m ** 2)

    # BMR
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Activity factor
    activity_factor = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.9
    }
    calories = bmr * activity_factor.get(activity, 1.2)

    # Goal adjustment
    if goal == "loss":
        calories -= 500
    elif goal == "gain":
        calories += 500

    # Age group
    if age <= 19:
        age_group = "Teen"
    elif age <= 50:
        age_group = "Adult"
    else:
        age_group = "Old"

    # BMI category + body type
    if bmi < 18.5:
        diet_type = "Weight Gain"
        body_type = "underweight"
    elif bmi <= 24.9:
        diet_type = "Balanced"
        body_type = "normal"
    elif bmi <= 29.9:
        diet_type = "Overweight"
        body_type = "overweight"
    else:
        diet_type = "Obese"
        body_type = "overweight"

    # Disease rules
    rules = []
    if disease == "diabetes":
        rules.append("Low Sugar Diet")
    elif disease == "bp":
        rules.append("Low Salt Diet")
    elif disease == "obesity":
        rules.append("Low Calorie Diet")
    elif disease == "hormonal":
        rules.append("High Protein, No Junk Food")

    # Age rules
    if age_group == "Teen":
        rules.append("High Energy & Protein")
    elif age_group == "Old":
        rules.append("Soft, Low Salt, Low Sugar")

    # Meal plan
    if goal == "loss":
        diet = {
            "Breakfast": "Oats + Fruits",
            "Lunch": "Chapati + Dal + Salad",
            "Dinner": "Soup + Salad"
        }
    elif goal == "gain":
        diet = {
            "Breakfast": "Milk + Banana + Peanut Butter",
            "Lunch": "Rice + Dal + Paneer",
            "Dinner": "Chapati + Curd"
        }
    else:
        diet = {
            "Breakfast": "Poha + Fruits",
            "Lunch": "Chapati + Dal",
            "Dinner": "Light Dinner"
        }

    # Image path
    image = f"images/{gender}_{body_type}.png"

    return bmi, calories, age_group, diet_type, rules, diet, image


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bmi, calories, age_group, diet_type, rules, diet, image = calculate(request.form)

        return render_template(
            "result.html",
            bmi=round(bmi, 2),
            calories=round(calories),
            age_group=age_group,
            diet_type=diet_type,
            rules=rules,
            diet=diet,
            image=image
        )

    return render_template("index.html")


# 🔥 IMPORTANT FOR RENDER DEPLOYMENT
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)