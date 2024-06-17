import sqlite3
import hashlib

class User:
    def __init__(self, username, password, name, age, weight, weight_goal): 
        self.username = username
        self.password = self.hash_password(password)
        self.name = name
        self.age = age
        self.weight = weight
        self.weight_goal = weight_goal

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_db(self):
        conn = sqlite3.connect('db_file')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users( 
                        username TEXT PRIMARY KEY,
                        password TEXT,
                        name TEXT,
                        age INTEGER,
                        weight REAL NOT NULL,
                        weight_goal REAL)''')
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
                       (self.username, self.password, self.name, self.age, self.weight, self.weight_goal))
        conn.commit()
        conn.close()

    @staticmethod
    def login(username, password):
        conn = sqlite3.connect('db_file')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data and user_data[1] == hashlib.sha256(password.encode()).hexdigest():
            return User(*user_data)
        else:
            return None

class Workout:
    def __init__(self, username, day, month, year, weight, exercises, sets, repetitions):
        self.username = username
        self.day = day
        self.month = month
        self.year = year
        self.weight = weight
        self.exercises = exercises
        self.sets = sets
        self.repetitions = repetitions

    def create_db(self):
        conn = sqlite3.connect('db_file')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS workouts(
                        username TEXT, 
                        day INTEGER, 
                        month INTEGER, 
                        year INTEGER,
                        weight REAL, 
                        exercises TEXT, 
                        sets INTEGER, 
                        repetitions INTEGER)''')
        cursor.execute("INSERT INTO workouts VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (self.username, self.day, self.month,                                                                                
                        self.year, self.weight, self.exercises,                                                                                
                        self.sets, self.repetitions))
        conn.commit()
        conn.close()

    @staticmethod
    def get_last_workout(username):
        conn = sqlite3.connect('db_file')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workouts WHERE username = ? ORDER BY year DESC, month DESC, day DESC", (username,))
        last_workout = cursor.fetchone()
        latest_date = [last_workout[1], last_workout[2], last_workout[3]]
        cursor.execute("SELECT * FROM workouts WHERE day = ? AND month = ? AND YEAR = ?", (latest_date[0], latest_date[1], latest_date[2]))
        latest_workout = cursor.fetchall()
        conn.close()
        size = len(latest_workout)
        print(f'Latest workout: {latest_date[0]}/{latest_date[1]}/{latest_date[2]} \nWeight: {latest_workout[0][4]}')
        for _ in range(size):
            print(f'Exercise: {latest_workout[_][5]} | Sets: {latest_workout[_][6]} | Repetitions: {latest_workout[_][7]}')

def home_page(username):
    conn = sqlite3.connect('db_file')
    cursor = conn.cursor()
    cursor.execute("SELECT name, weight, weight_goal FROM users WHERE username = ? ORDER BY weight DESC, weight_goal DESC LIMIT 1", (username,))
    home = cursor.fetchone()
    conn.close()
    return f'name: {home[0]} \nweight: {home[1]} \nweight_goal: {home[2]}'

def edit_profile(username):
    conn = sqlite3.connect('db_file')
    cursor = conn.cursor()
    
    print("What do you want to change?")
    print("")
    print("[1]Name \n[2]Password \n[3]Weight \n[4]Weight Goal")
    print("")
    
    x = input("Type: ")
    print("")
    
    if x == '1':
        new_name = input("New name: ")
        cursor.execute("UPDATE users SET name = ? WHERE username = ?", (new_name, username))
        conn.commit()
        print("Name changed successfully!")
        conn.close()

    if x == '2':
        password = input("New password: ")
        hashed = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
        conn.commit()
        print("Password changed successfully!")
        conn.close()

    if x == '3':
        new_weight = input("New weight: ")
        cursor.execute("UPDATE users SET weight = ? WHERE username = ?", (new_weight, username))
        conn.commit()
        print("Weight changed successfully!")
        conn.close()

    if x == '4':
        new_weight_goal = input("New weight goal: ")
        cursor.execute("UPDATE users SET weight_goal = ? WHERE username = ?", (new_weight_goal, username))
        conn.commit()
        print("Weight goal changed successfully!")
        conn.close()

def search(username):
    conn = sqlite3.connect('db_file')
    cursor = conn.cursor()
    day = int(input("Day: "))
    month = int(input("Month: "))
    year = int(input("Year: "))
    print("")
    cursor.execute("SELECT weight, exercises, sets, repetitions FROM workouts WHERE username = ? AND day = ? AND month = ? AND year = ? ", (username, day, month, year))
    searching = cursor.fetchall() 
    conn.close()
    print(f'weight: {searching[0][0]}')
    size = len(searching)
    for _ in range(size): 
        print(f'Exercise: {searching[_][1]} | Sets: {searching[_][2]} | Repetitions: {searching[_][3]}')
