from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import random
import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(
    api_key=GEMINI_API_KEY
)

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "health.db")
def init_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            height REAL NOT NULL,
            weight REAL NOT NULL,
            diet TEXT NOT NULL,
            activity TEXT NOT NULL,
            goal TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


init_database()


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def serve_page(filename):
    return send_from_directory(BASE_DIR, filename)


@app.route("/api/profile", methods=["POST"])
def save_profile():
    data = request.get_json()

    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    height = data.get("height")
    weight = data.get("weight")
    diet = data.get("diet")
    activity = data.get("activity")
    goal = data.get("goal")

    if not all([
        name, age, gender, height,
        weight, diet, activity, goal
    ]):
        return jsonify({
            "success": False,
            "message": "All profile fields are required."
        }), 400

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users
        (name, age, gender, height, weight, diet, activity, goal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        gender,
        height,
        weight,
        diet,
        activity,
        goal
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Profile saved successfully!"
    })
@app.route("/api/meal-plan", methods=["GET"])
def get_meal_plan():

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, age, gender, height, weight, diet, activity, goal
        FROM users
        ORDER BY rowid DESC
        LIMIT 1
    """)

    user = cursor.fetchone()
    connection.close()

    if not user:
        return jsonify({
            "success": False,
            "message": "No profile found."
        }), 404

    # -----------------------------
    # USER INFORMATION
    # -----------------------------

    diet = (user["diet"] or "").lower()
    goal = (user["goal"] or "").lower()

    age = float(user["age"])
    height = float(user["height"])
    weight = float(user["weight"])
    gender = (user["gender"] or "").lower()
    activity = (user["activity"] or "").lower()

    # -----------------------------
    # CALORIE CALCULATION
    # -----------------------------

    if gender == "female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    activity_multiplier = 1.2

    if activity == "light":
        activity_multiplier = 1.375
    elif activity == "moderate":
        activity_multiplier = 1.55
    elif activity == "active":
        activity_multiplier = 1.725

    daily_calories = bmr * activity_multiplier

    if "lose" in goal or "loss" in goal:
        daily_calories -= 300
    elif "gain" in goal:
        daily_calories += 300

    daily_calories = round(daily_calories)

    breakfast_calories = round(daily_calories * 0.25)
    lunch_calories = round(daily_calories * 0.35)
    snack_calories = round(daily_calories * 0.15)
    dinner_calories = round(daily_calories * 0.25)

# -----------------------------
    # MEAL PLAN
    # -----------------------------

    breakfast_options = [
        {"name": "Poha with Peanuts", "description": "Light poha cooked with vegetables and topped with roasted peanuts."},
        {"name": "Vegetable Upma", "description": "Soft semolina upma prepared with mixed vegetables and mild spices."},
        {"name": "Masala Oats", "description": "Savory oats cooked with vegetables and Indian spices."},
        {"name": "Moong Dal Chilla", "description": "Protein-rich moong dal pancakes served with fresh chutney."},
        {"name": "Idli with Sambar", "description": "Steamed idlis served with warm vegetable sambar."},
        {"name": "Vegetable Paratha with Curd", "description": "Homemade vegetable paratha served with fresh curd."},
        {"name": "Besan Chilla", "description": "Savory gram-flour pancakes prepared with onions and vegetables."},
        {"name": "Dosa with Sambar", "description": "Crispy dosa served with nutritious sambar and chutney."},
        {"name": "Vegetable Uttapam", "description": "Soft uttapam topped with fresh vegetables and served with chutney."},
        {"name": "Ragi Dosa", "description": "Crispy ragi dosa served with vegetable sambar and chutney."},
        {"name": "Sabudana Khichdi", "description": "Soft sabudana cooked with peanuts, potatoes and mild spices."},
        {"name": "Vegetable Vermicelli", "description": "Vermicelli cooked with mixed vegetables and light Indian spices."},
        {"name": "Methi Paratha with Curd", "description": "Methi parathas served with fresh curd and a light vegetable side."},
        {"name": "Aloo Paratha with Curd", "description": "Stuffed potato paratha served with fresh curd."},
        {"name": "Sprouts Poha", "description": "Vegetable poha topped with nutritious sprouts and peanuts."},
        {"name": "Dal Chilla with Chutney", "description": "Crispy lentil pancakes served with fresh mint chutney."},
        {"name": "Vegetable Sandwich", "description": "Whole-grain vegetable sandwich filled with fresh crunchy vegetables."},
        {"name": "Corn and Vegetable Upma", "description": "Savory upma prepared with vegetables and sweet corn."},
        {"name": "Oats Chilla", "description": "Savory oats pancakes prepared with vegetables and herbs."},
        {"name": "Rice Idli with Sambar", "description": "Soft steamed rice idlis served with warm vegetable sambar."}
    ]

    lunch_options = [
        {"name": "Dal Rice with Salad", "description": "Comforting dal and rice served with a fresh vegetable salad."},
        {"name": "Rajma Rice", "description": "Kidney bean curry served with steamed rice and fresh salad."},
        {"name": "Vegetable Pulao with Raita", "description": "Fragrant vegetable pulao served with refreshing raita."},
        {"name": "Chapati with Dal and Sabzi", "description": "Whole-wheat chapatis served with dal and seasonal vegetables."},
        {"name": "Chole with Roti", "description": "Spiced chickpea curry served with fresh whole-wheat roti."},
        {"name": "Paneer Bhurji with Roti", "description": "Spiced paneer bhurji served with whole-wheat rotis and salad."},
        {"name": "Khichdi with Curd", "description": "Balanced rice and lentil khichdi served with fresh curd."},
        {"name": "Vegetable Biryani with Raita", "description": "Aromatic vegetable biryani served with cooling raita."},
        {"name": "Dal Tadka with Jeera Rice", "description": "Yellow dal tadka served with fragrant cumin rice and salad."},
        {"name": "Palak Paneer with Roti", "description": "Spinach and paneer curry served with whole-wheat rotis."},
        {"name": "Kadhi Rice", "description": "Light yogurt-based kadhi served with steamed rice and vegetables."},
        {"name": "Vegetable Khichdi", "description": "Rice and lentils cooked with mixed vegetables and mild spices."},
        {"name": "Matar Paneer with Roti", "description": "Green peas and paneer curry served with whole-wheat rotis."},
        {"name": "Dal Fry with Roti", "description": "Flavorful dal fry served with whole-wheat rotis and salad."},
        {"name": "Vegetable Korma with Roti", "description": "Mixed vegetables cooked in a mild gravy with whole-wheat roti."},
        {"name": "Chana Masala Rice", "description": "Chickpea curry served with steamed rice and fresh salad."},
        {"name": "Lemon Rice with Dal", "description": "Tangy lemon rice served with a comforting lentil preparation."},
        {"name": "Soya Chunk Curry with Roti", "description": "Protein-rich soya chunks cooked in a homestyle curry with roti."},
        {"name": "Vegetable Handvo with Curd", "description": "Savory vegetable handvo served with fresh curd."},
        {"name": "Moong Dal Khichdi", "description": "Light moong dal khichdi served with vegetables and salad."}
    ]

    snack_options = [
        {"name": "Roasted Makhana", "description": "Crunchy roasted makhana seasoned with mild spices."},
        {"name": "Fruit Bowl", "description": "A refreshing bowl of seasonal fruits."},
        {"name": "Sprouts Chaat", "description": "Fresh sprouts mixed with vegetables, lemon and mild spices."},
        {"name": "Roasted Chana", "description": "Crunchy roasted chickpeas providing a simple protein-rich snack."},
        {"name": "Peanut Chaat", "description": "Boiled peanuts mixed with onion, tomato and lemon."},
        {"name": "Banana with Peanut Butter", "description": "A banana paired with a small serving of peanut butter."},
        {"name": "Corn Chaat", "description": "Sweet corn mixed with vegetables, lemon and mild spices."},
        {"name": "Curd with Fruit", "description": "Fresh curd served with chopped seasonal fruit."},
        {"name": "Apple and Nuts", "description": "Fresh apple served with a small portion of mixed nuts."},
        {"name": "Buttermilk with Roasted Chana", "description": "Refreshing buttermilk paired with crunchy roasted chana."},
        {"name": "Cucumber Chaat", "description": "Fresh cucumber mixed with lemon, herbs and mild spices."},
        {"name": "Guava with Chaat Masala", "description": "Fresh guava slices seasoned lightly with chaat masala."},
        {"name": "Almonds and Fruit", "description": "Seasonal fruit served with a small handful of almonds."},
        {"name": "Boiled Corn", "description": "Warm boiled corn seasoned with lemon and mild spices."},
        {"name": "Chana Chaat", "description": "Boiled chickpeas mixed with tomato, onion and lemon."},
        {"name": "Yogurt and Fruit", "description": "Fresh yogurt combined with chopped seasonal fruit."},
        {"name": "Roasted Peanuts", "description": "Crunchy roasted peanuts served as a simple protein-rich snack."},
        {"name": "Carrot and Cucumber Sticks", "description": "Fresh carrot and cucumber sticks served with a light dip."},
        {"name": "Fruit Smoothie", "description": "Fresh seasonal fruit blended into a simple smoothie."},
        {"name": "Dates and Almonds", "description": "A small serving of dates paired with almonds."}
    ]

    dinner_options = [
        {"name": "Dal Khichdi with Salad", "description": "Light dal khichdi served with a fresh vegetable salad."},
        {"name": "Roti with Mixed Vegetable Curry", "description": "Whole-wheat rotis served with a nutritious mixed vegetable curry."},
        {"name": "Paneer Tikka with Salad", "description": "Grilled paneer tikka served with a fresh crunchy salad."},
        {"name": "Dal with Roti and Sabzi", "description": "Wholesome dal served with rotis and seasonal vegetables."},
        {"name": "Vegetable Soup with Roti", "description": "Warm vegetable soup served with a small portion of whole-wheat roti."},
        {"name": "Palak Paneer with Roti", "description": "Spinach and paneer curry served with whole-wheat rotis."},
        {"name": "Vegetable Dalia", "description": "Light broken-wheat dalia cooked with mixed vegetables."},
        {"name": "Chana Masala with Roti", "description": "Chickpea curry served with whole-wheat rotis and salad."},
        {"name": "Lauki Dal with Roti", "description": "Light bottle-gourd dal served with whole-wheat rotis."},
        {"name": "Vegetable Stir Fry with Roti", "description": "Mixed vegetables lightly stir-fried and served with whole-wheat roti."},
        {"name": "Moong Dal with Rice", "description": "Light moong dal served with steamed rice and fresh vegetables."},
        {"name": "Matar Paneer with Roti", "description": "Green peas and paneer curry served with whole-wheat rotis."},
        {"name": "Tawa Vegetable with Roti", "description": "Mixed vegetables cooked on a tawa and served with roti."},
        {"name": "Soya Curry with Rice", "description": "Protein-rich soya curry served with steamed rice and salad."},
        {"name": "Dal Tadka with Jeera Rice", "description": "Dal tadka served with fragrant cumin rice and vegetables."},
        {"name": "Vegetable Pulao with Raita", "description": "Light vegetable pulao served with refreshing raita."},
        {"name": "Stuffed Vegetable Roti", "description": "Whole-wheat roti stuffed with seasoned vegetables and served with curd."},
        {"name": "Tomato Soup with Paneer Salad", "description": "Warm tomato soup served with a fresh paneer and vegetable salad."},
        {"name": "Mixed Dal with Roti", "description": "Mixed lentil curry served with whole-wheat rotis and salad."},
        {"name": "Vegetable Oats Khichdi", "description": "Light oats khichdi cooked with lentils and mixed vegetables."}
    ]

    # -----------------------------
    # NON-VEGETARIAN OPTIONS
    # -----------------------------

    if diet == "non-vegetarian":
        breakfast_options = [
            {"name": "Egg Bhurji with Toast", "description": "Scrambled eggs with vegetables served with whole-grain toast."},
            {"name": "Masala Omelette with Toast", "description": "Vegetable masala omelette served with whole-grain toast."},
            {"name": "Boiled Eggs with Toast", "description": "Boiled eggs served with whole-grain toast and vegetables."},
            {"name": "Chicken Sandwich", "description": "Whole-grain sandwich filled with seasoned chicken and vegetables."},
            {"name": "Egg Sandwich", "description": "Whole-grain sandwich filled with boiled egg and fresh vegetables."},
            {"name": "Chicken Omelette", "description": "Egg omelette with small pieces of seasoned chicken and vegetables."}
        ]

        lunch_options = [
            {"name": "Chicken Rice Bowl", "description": "Seasoned chicken served with rice and fresh vegetables."},
            {"name": "Chicken Roti Bowl", "description": "Grilled chicken served with whole-wheat roti and salad."},
            {"name": "Chicken Curry with Rice", "description": "Homestyle chicken curry served with steamed rice and salad."},
            {"name": "Egg Curry with Roti", "description": "Egg curry served with whole-wheat rotis and vegetables."},
            {"name": "Chicken Biryani with Raita", "description": "Aromatic chicken biryani served with a moderate portion of raita."},
            {"name": "Fish Curry with Rice", "description": "Light fish curry served with steamed rice and vegetables."},
            {"name": "Chicken Tikka with Roti", "description": "Grilled chicken tikka served with whole-wheat roti and salad."}
        ]

        snack_options = [
            {"name": "Boiled Eggs", "description": "Boiled eggs served with a light vegetable side."},
            {"name": "Egg Chaat", "description": "Boiled eggs mixed with vegetables, lemon and mild spices."},
            {"name": "Chicken Salad", "description": "Small serving of grilled chicken with fresh vegetables."},
            {"name": "Fruit with Boiled Egg", "description": "Seasonal fruit served with a boiled egg."},
            {"name": "Yogurt with Fruit", "description": "Fresh yogurt served with chopped seasonal fruit."}
        ]

        dinner_options = [
            {"name": "Grilled Chicken with Roti", "description": "Grilled chicken served with whole-wheat roti and vegetables."},
            {"name": "Chicken Curry with Roti", "description": "Homestyle chicken curry served with whole-wheat rotis."},
            {"name": "Chicken Stir Fry with Rice", "description": "Chicken stir-fried with vegetables and served with rice."},
            {"name": "Fish Curry with Rice", "description": "Light fish curry served with steamed rice and vegetables."},
            {"name": "Egg Curry with Roti", "description": "Egg curry served with whole-wheat rotis and vegetables."},
            {"name": "Chicken Tikka with Salad", "description": "Grilled chicken tikka served with a fresh vegetable salad."},
            {"name": "Chicken Rice Bowl", "description": "Seasoned chicken served with rice and fresh vegetables."}
        ]

    # -----------------------------
    # VEGAN FILTER
    # -----------------------------

    if diet == "vegan":
        non_vegan_words = [
            "curd",
            "yogurt",
            "paneer",
            "raita",
            "milk",
            "cheese",
            "butter",
            "ghee",
            "egg",
            "chicken",
            "fish",
            "meat"
        ]

        breakfast_options = [
            meal for meal in breakfast_options
            if not any(
                word in (meal["name"] + " " + meal["description"]).lower()
                for word in non_vegan_words
            )
        ]

        lunch_options = [
            meal for meal in lunch_options
            if not any(
                word in (meal["name"] + " " + meal["description"]).lower()
                for word in non_vegan_words
            )
        ]

        snack_options = [
            meal for meal in snack_options
            if not any(
                word in (meal["name"] + " " + meal["description"]).lower()
                for word in non_vegan_words
            )
        ]

        dinner_options = [
            meal for meal in dinner_options
            if not any(
                word in (meal["name"] + " " + meal["description"]).lower()
                for word in non_vegan_words
            )
        ]

    # -----------------------------
    # RANDOM MEAL SELECTION
    # -----------------------------

    breakfast = random.choice(breakfast_options)
    lunch = random.choice(lunch_options)
    snack = random.choice(snack_options)
    dinner = random.choice(dinner_options)

    # -----------------------------
    # RETURN COMPLETE MEAL PLAN
    # -----------------------------

    return jsonify({
        "success": True,

        "user": {
            "name": user["name"],
            "goal": user["goal"],
            "diet": user["diet"]
        },

        "daily_calories": daily_calories,

        "meals": {
            "breakfast": {
                "name": breakfast["name"],
                "description": breakfast["description"],
                "calories": breakfast_calories
            },

            "lunch": {
                "name": lunch["name"],
                "description": lunch["description"],
                "calories": lunch_calories
            },

            "snack": {
                "name": snack["name"],
                "description": snack["description"],
                "calories": snack_calories
            },

            "dinner": {
                "name": dinner["name"],
                "description": dinner["description"],
                "calories": dinner_calories
            }
        }
    })
# ===============================
# AI SYMPTOM WELLNESS GUIDE
# ===============================

@app.route("/api/symptoms", methods=["POST"])
def symptom_guide():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Please provide your symptoms."
        }), 400

    symptoms = data.get("symptoms", "").strip().lower()
    age = data.get("age")
    gender = data.get("gender")
    height = data.get("height")
    weight = data.get("weight")
    diet = data.get("diet")
    activity = data.get("activity")
    goal = data.get("goal")
    # Calculate BMI when profile information is available
    bmi = None

    try:
        if height and weight:
            height_m = float(height) / 100
            bmi = round(float(weight) / (height_m * height_m), 1)
    except (ValueError, TypeError, ZeroDivisionError):
        bmi = None
    # -----------------------------
    # URGENT SYMPTOM CHECK
    # -----------------------------

    urgent_words = [
        "chest pain",
        "difficulty breathing",
        "can't breathe",
        "cannot breathe",
        "severe bleeding",
        "unconscious",
        "fainted",
        "seizure",
        "stroke",
        "suicidal"
    ]

    if any(word in symptoms for word in urgent_words):

        return jsonify({
            "success": True,
            "guidance": (
                "Your description may include a potentially serious symptom. "
                "This application cannot assess emergencies or diagnose conditions. "
                "Please seek urgent medical attention or contact your local emergency service."
            )
        })

    if not symptoms:
        return jsonify({
            "success": False,
            "message": "Please describe your symptoms first."
        }), 400
    profile_note = ""

    if bmi is not None:
        profile_note += f" Your current BMI is {bmi}."

    if goal:
        profile_note += f" Your current health goal is {goal}."

    if activity:
        profile_note += f" Your activity level is {activity}."

    if diet:
        profile_note += f" Your diet preference is {diet}."

# -----------------------------
    # GENERAL WELLNESS GUIDANCE
    # -----------------------------

    prompt = f"""
You are a wellness assistant inside an AI Nutritional Healthcare app.

The user described these symptoms:
{symptoms}

User profile:
Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
Diet: {diet}
Activity level: {activity}
Health goal: {goal}
BMI: {bmi}

Give concise, easy-to-understand general wellness guidance.

Rules:
- Do NOT diagnose a disease or medical condition.
- Do NOT prescribe medication or treatment.
- Do NOT claim certainty about the cause of symptoms.
- Suggest practical general wellness steps such as hydration, rest,
  balanced nutrition, and monitoring symptoms when appropriate.
- Tell the user to consult a healthcare professional if symptoms are
  persistent, severe, worsening, or concerning.
- If the symptoms sound potentially urgent, advise seeking urgent
  medical attention.
- Do not overreact to ordinary mild symptoms.
- Keep the response around 100-150 words.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "temperature": 0.3,
                "max_output_tokens": 200
            }
        )

        guidance = response.text.strip()

    except Exception as error:
        print("Gemini Error:", error)

        return jsonify({
            "success": False,
            "message": "The AI wellness service is temporarily unavailable. Please try again."
        }), 503

    return jsonify({
        "success": True,
        "guidance": guidance
    })


if __name__=="__main__":
    app.run(debug=True)


