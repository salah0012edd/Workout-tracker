import sqlite3


conn = None
cursor = None

def open(db_name):
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    conn.close()

def do(query, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()

# Create Workouts and Meals tables
def createWO():
    open('workouts.db')
    cursor.execute('PRAGMA foreign_keys=ON')

    # Workouts table
    do('''CREATE TABLE IF NOT EXISTS Workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercice TEXT NOT NULL,
            date DATE NOT NULL,
            sets INTEGER,
            reps INTEGER,
            duration INTEGER
        )''')
    close()
def createME():
    open('meals.db')
    # Meals table
    do('''CREATE TABLE IF NOT EXISTS Meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_name TEXT NOT NULL,
            calories INTEGER,
            protein INTEGER,
            date DATE NOT NULL
        )''')
    
    close()

# Insert into Workouts table
def insert_workout(exercice, date, sets, reps, duration):
    open('workouts.db')
    do("INSERT INTO Workouts (exercice, date, sets, reps, duration) VALUES (?, ?, ?, ?, ?)", 
       (exercice, date, sets, reps, duration))
    close()

# Insert into Meals table
def insert_meal(meal_name, calories, protein, date):
    open('meals.db')
    do("INSERT INTO Meals (meal_name, calories, protein, date) VALUES (?, ?, ?, ?)", 
       (meal_name, calories, protein, date))
    close()

# Show data from a table
def showDB(table):
    query = f'SELECT * FROM {table}'
    open('workouts.db')
    cursor.execute(query)
    print(cursor.fetchall())
    close()

# Show tables
def show_tablesDB():
    print("Workouts:")
    showDB('Workouts')
    print("Meals:")
    showDB('Meals')

# Update workouts or meals
def update_workout(id, exercice=None, date=None, sets=None, reps=None, duration=None):
    open('workouts.db')
    updates = []
    params = []
    
    if exercice:
        updates.append("exercice = ?")
        params.append(exercice)
    if date:
        updates.append("date = ?")
        params.append(date)
    if sets is not None:
        updates.append("sets = ?")
        params.append(sets)
    if reps is not None:
        updates.append("reps = ?")
        params.append(reps)
    if duration is not None:
        updates.append("duration = ?")
        params.append(duration)

    params.append(id)
    
    query = f"UPDATE Workouts SET {', '.join(updates)} WHERE id = ?"
    do(query, params)
    close()

def update_meal(id, meal_name=None, calories=None, protein=None, date=None):
    open('meals.db')
    updates = []
    params = []
    
    if meal_name:
        updates.append("meal_name = ?")
        params.append(meal_name)
    if calories is not None:
        updates.append("calories = ?")
        params.append(calories)
    if protein is not None:
        updates.append("protein = ?")
        params.append(protein)
    if date:
        updates.append("date = ?")
        params.append(date)

    params.append(id)
    
    query = f"UPDATE Meals SET {', '.join(updates)} WHERE id = ?"
    do(query, params)
    close()

# Delete from workouts or meals
def delete_workout(id):
    open('workouts.db')
    do("DELETE FROM Workouts WHERE id = ?", (id,))
    close()

def delete_meal(id):
    open('meals.db')
    do("DELETE FROM Meals WHERE id = ?", (id,))
    close()

# Clear auto-increment IDs
def clear_ids(table):
    open('workouts.db')
    do(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
    close()

# Clear all data
def clear_all():
    open('workouts.db')
    open('meals.db')
    do("DELETE FROM Workouts")
    do("DELETE FROM Meals")
    clear_ids("Workouts")
    clear_ids("Meals")
    close()
    close()