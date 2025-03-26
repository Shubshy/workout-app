from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)

# File paths
WORKOUTS_FILE = "workouts.json"
PROGRAM_FILE = "weekly_program.json"

# Load data functions
def load_workouts():
    if os.path.exists(WORKOUTS_FILE):
        with open(WORKOUTS_FILE, "r") as f:
            return json.load(f)
    return []

def load_program():
    if os.path.exists(PROGRAM_FILE):
        with open(PROGRAM_FILE, "r") as f:
            return json.load(f)
    return {
        "Monday": "Rest",
        "Tuesday": "Rest",
        "Wednesday": "Rest",
        "Thursday": "Rest",
        "Friday": "Rest",
        "Saturday": "Rest",
        "Sunday": "Rest"
    }

# Save data functions
def save_workouts(data):
    with open(WORKOUTS_FILE, "w") as f:
        json.dump(data, f)

def save_program(data):
    with open(PROGRAM_FILE, "w") as f:
        json.dump(data, f)

# Routes
@app.route("/")
def home():
    return render_template("index.html", 
                         workouts=load_workouts(),
                         program=load_program())

@app.route("/add", methods=["POST"])
def add_workout():
    workout = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": request.form["name"],
        "weight": request.form["weight"],
        "sets": request.form["sets"],
        "reps": request.form["reps"],
        "notes": request.form["notes"]
    }
    workouts = load_workouts()
    workouts.append(workout)
    save_workouts(workouts)
    return redirect(url_for("home"))

@app.route("/search", methods=["POST"])
def search():
    date = request.form["search_date"]
    workouts = [w for w in load_workouts() if w["date"].startswith(date)]
    return render_template("index.html", 
                         workouts=workouts,
                         program=load_program(),
                         search_date=date)

@app.route("/update_program", methods=["POST"])
def update_program():
    program = {day: request.form[day] for day in load_program()}
    save_program(program)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)