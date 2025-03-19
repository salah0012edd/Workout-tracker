from flask import Flask, render_template, request, redirect, url_for, send_from_directory  # noqa: F401; flake8: ignoreder
from database import sqlite3,delete_meal, delete_workout, insert_meal,insert_workout,update_meal,update_workout,createME,createWO

app = Flask(__name__,template_folder='template')


def db_connection():
    conn_meals = sqlite3.connect('Meals.db')
    conn_Workouts = sqlite3.connect('Workouts.db')
   
    # telling SQLite to return the results as Row objects instead of tuples
    # make it easy to access the values in tasks
    conn_Workouts.row_factory = sqlite3.Row
    conn_meals.row_factory = sqlite3.Row
    return conn_meals, conn_Workouts

@app.route('/')    
def index():
    conn_meals, conn_Workouts = db_connection()
    meals = conn_meals.execute("SELECT * FROM Meals").fetchall()
    workout = conn_Workouts.execute("SELECT * FROM Workouts").fetchall()
    
    conn_Workouts.close()
    conn_meals.close()
    return render_template('index.html', workouts=workout, meal=meals)

@app.route('/add_workout', methods=['POST'])
def add_workout():
    exercise = request.form['exercice']
    date = request.form['date']
    set = request.form['sets']
    rep = request.form['reps']
    duration = request.form['duration']
    _, conn_Workouts = db_connection()
    insert_workout(exercise, date, set, rep, duration)
    conn_Workouts.close()
    return redirect(url_for('index'))

@app.route('/add_', methods=['POST'])
def add_meal():
    meal_name = request.form['meal_name']
    calories = request.form['calories']
    protein = request.form['protein']
    date = request.form['date']
    conn_meals, _ = db_connection()
    insert_meal(meal_name, calories, protein, date)
    conn_meals.close()
    return redirect(url_for('index'))

@app.route("/update_workout/<int:id>", methods=["POST"])
def update_wor(id):
    conn_Workouts, _ = db_connection()
    update_workout(id, request.form['exercice'], request.form['date'], request.form['sets'], request.form['reps'], request.form['duration'])
    conn_Workouts.close()
    return redirect(url_for('index'))

@app.route("/update_meal/<int:id>", methods=["POST"])
def update_meal(id):
    conn_meals, _ = db_connection()
    update_meal(id, request.form['meal_name'], request.form['calories'], request.form['protein'], request.form['date'])
    conn_meals.close()
    return redirect(url_for('index'))

@app.route("/delete_workout/<int:id>")
def delete_wor(id):
    _, conn_Workouts = db_connection()
    delete_workout(id)
    conn_Workouts.close()
    return redirect(url_for('index'))

@app.route("/delete_meal/<int:id>")
def delete_me(id):
    conn_meals, _ = db_connection()
    delete_meal(id)
    conn_meals.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    createWO()
    createME()
    app.run(debug=True)