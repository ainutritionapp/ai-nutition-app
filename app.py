from flask import Flask, render_template, request, send_file
import random
import io
import json
import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

app = Flask(__name__)

# ---------- SAFE CONVERSION ----------
def to_int(val, default=0):
    try:
        if val is None or val == "":
            return default
        return int(float(val))
    except:
        return default

def to_float(val, default=0.0):
    try:
        if val is None or val == "":
            return default
        return float(val)
    except:
        return default


# ---------- CALCULATION ----------
def calculate(data):
    name = data.get("name") or "User"
    age = to_int(data.get("age"))
    weight = to_float(data.get("weight"))
    height = to_float(data.get("height"))

    gender = data.get("gender") or "male"
    activity = data.get("activity") or "low"
    goal = data.get("goal") or "loss"
    disease = data.get("disease") or "none"

    if height <= 0:
        height = 150

    height_m = height / 100
    bmi = weight / (height_m ** 2) if weight else 0

    # BMR
    if gender == "male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    activity_map = {"low":1.2,"medium":1.55,"high":1.9}
    calories = bmr * activity_map.get(activity,1.2)

    if goal == "loss":
        calories -= 400
    elif goal == "gain":
        calories += 400

    protein = round(weight * 1.6) if weight else 0
    fats = round(weight * 0.8) if weight else 0
    carbs = round((calories - (protein*4 + fats*9)) / 4) if calories else 0

    # Category
    if bmi < 18.5:
        category = "Underweight"
    elif bmi <= 24.9:
        category = "Normal"
    elif bmi <= 29.9:
        category = "Overweight"
    else:
        category = "Obese"

    advice = "Maintain healthy lifestyle"

    image = f"images/{gender}_normal.png"

    # Weekly Diet
    breakfast = ["Oats + Fruits","Poha + Peanuts","Upma","Idli + Sambar"]
    lunch = ["Chapati + Dal + Salad","Rice + Sabzi","Khichdi","Curd Rice"]
    dinner = ["Soup + Salad","Chapati + Sabzi","Light Dal Rice","Vegetable Soup"]

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    weekly = {}
    for d in days:
        weekly[d] = {
            "Breakfast": random.choice(breakfast),
            "Lunch": random.choice(lunch),
            "Dinner": random.choice(dinner)
        }

    return name, age, bmi, calories, protein, carbs, fats, category, advice, image, weekly, disease


# ---------- ROUTES ----------
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        result = calculate(request.form)

        return render_template("result.html",
            name=result[0],
            age=result[1],
            bmi=round(result[2],2),
            calories=round(result[3]),
            protein=result[4],
            carbs=result[5],
            fats=result[6],
            category=result[7],
            advice=result[8],
            image=result[9],
            weekly=result[10],
            disease=result[11]
        )

    return render_template("index.html")


# ---------- PDF ----------
@app.route("/download_pdf", methods=["POST"])
def download_pdf():

    name = request.form.get("name") or "User"
    age = request.form.get("age") or "0"
    bmi = request.form.get("bmi") or "0"
    calories = request.form.get("calories") or "0"
    category = request.form.get("category") or ""
    protein = request.form.get("protein") or "0"
    carbs = request.form.get("carbs") or "0"
    fats = request.form.get("fats") or "0"
    disease = request.form.get("disease") or "none"

    # SAFE WEEKLY
    try:
        weekly = json.loads(request.form.get("weekly") or "{}")
    except:
        weekly = {}

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    safe_weekly = {}
    for d in days:
        data = weekly.get(d, {})
        safe_weekly[d] = {
            "Breakfast": str(data.get("Breakfast") or "-"),
            "Lunch": str(data.get("Lunch") or "-"),
            "Dinner": str(data.get("Dinner") or "-")
        }

    weekly = safe_weekly

    today = datetime.date.today().strftime("%d %B %Y")

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    title = ParagraphStyle(name='t', fontSize=22, alignment=TA_CENTER)
    report = ParagraphStyle(name='r', fontSize=16, alignment=TA_CENTER, italic=True)
    left = ParagraphStyle(name='l', fontSize=12, alignment=TA_LEFT)
    right = ParagraphStyle(name='rr', fontSize=12, alignment=TA_RIGHT)

    elements = []

    elements.append(Paragraph("<b>AI Nutrition App</b>", title))
    elements.append(Spacer(1,10))
    elements.append(HRFlowable(width="100%", thickness=1))
    elements.append(Spacer(1,15))

    elements.append(Table([
        [
            Paragraph(f"<b>{name}</b><br/>Age: {age}", left),
            Paragraph("<b><i>Health Report</i></b>", report),
            Paragraph(today, right)
        ]
    ], colWidths=[5*cm,6*cm,5*cm]))

    elements.append(Spacer(1,15))
    elements.append(HRFlowable(width="100%", thickness=0.5))
    elements.append(Spacer(1,15))

    # LEFT RIGHT BLOCK
    elements.append(Table([
        [
            Paragraph(f"<b>BMI:</b> {bmi}<br/>Category: {category}<br/>Calories: {calories}<br/>Disease: {disease}", left),
            "",
            Paragraph(f"<b>Macronutrients</b><br/>Protein: {protein}g<br/>Carbs: {carbs}g<br/>Fats: {fats}g", left)
        ]
    ], colWidths=[7.5*cm,0.2*cm,7.5*cm]))

    elements.append(Spacer(1,15))

    # SAFE TABLE
    table_data = [["Day","Breakfast","Lunch","Dinner"]]

    for d in days:
        m = weekly[d]
        table_data.append([d, m["Breakfast"], m["Lunch"], m["Dinner"]])

    table = Table(table_data, colWidths=[4*cm,5*cm,4.5*cm,4.5*cm])

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="Health_Report.pdf")


# ---------- RUN ----------
if __name__ == "__main__":
    app.run()
