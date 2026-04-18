# 🥗 AI Nutrition Recommendation System

## 📌 Project Overview

This project is a simple AI-based Nutrition Recommendation System that provides personalized diet suggestions based on user inputs such as age, weight, height, gender, and fitness goals.

The system performs:

* BMI calculation
* Daily calorie requirement estimation
* Goal-based diet recommendations

---

## ⚙️ Features

* BMI Calculation
* BMI Category Classification (Underweight / Normal / Overweight)
* Daily Calorie Requirement Calculation
* Goal-based Diet Plan (Weight Loss / Weight Gain / Maintenance)
* Simple and User-Friendly Web Interface (Flask + Bootstrap)

---

## 🛠️ Technologies Used

* Python
* Flask
* Pandas
* HTML
* Bootstrap

---

## 📁 Project Structure

```plaintext
AI-Nutrition-System/
│
├── app.py              # Flask web application
├── main.py             # CLI version
├── diet_data.csv       # Food dataset
├── requirements.txt    # Required libraries
│
└── templates/
    ├── index.html      # Input form page
    └── result.html     # Output result page
```

---

## 💻 Installation Guide

### Step 1: Install Python

Make sure Python is installed on your system:

```bash
python --version
```

---

### Step 2: Setup Project

Download or copy the project folder to your system.

---

### Step 3: Install Dependencies

Run the following command in terminal:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Project

### 🔹 Option 1: Run CLI Version

```bash
python main.py
```

---

### 🔹 Option 2: Run Web Application (Recommended)

```bash
python app.py
```

Then open your browser and go to:

```bash
http://127.0.0.1:5000
```

---

## 🧪 Sample Input

* Age: 25
* Weight: 70 kg
* Height: 170 cm
* Gender: Male
* Goal: Weight Loss

---

## 📊 Output

The system provides:

* BMI value
* BMI category
* Daily calorie requirement
* Recommended diet plan

---

## ⚠️ Common Issues & Solutions

### ❌ ModuleNotFoundError

Install required libraries:

```bash
pip install pandas flask
```

---

### ❌ TemplateNotFound Error

Make sure:

* `templates` folder exists
* HTML files are inside the `templates` folder

---

## 🚀 Future Enhancements

* User authentication system
* Diet history tracking
* Advanced AI/ML-based recommendations
* Mobile-friendly UI

---

## 👨‍💻 Author

Developed as a college project for learning AI-based recommendation systems.

---
