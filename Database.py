# Importing necessary libraries
# import pickle  # Unused import, can be removed
import sqlite3
from numpy import False_

# Connecting to the SQLite database
liconn = sqlite3.connect("list.db")
licr = liconn.cursor()

# Creating a table if it doesn't exist
licr.execute("""CREATE TABLE IF NOT EXISTS list(
        id INTEGER PRIMARY KEY ,
        name TEXT,
        last_name TEXT,
        phone_number TEXT UNIQUE,
        night_permi INTEGER,
        night_stay INTEGER    
    )""")
liconn.commit()

# Function to get a user by their ID
def get_by_id(id):
    licr.execute("SELECT * FROM list WHERE id==?", (id,))
    return licr.fetchone()

# Function to get a user by their phone number
def get_by_number(phonenumber):
    licr.execute("SELECT * FROM list WHERE phone_number==?", (phonenumber,))
    return licr.fetchone()

# Function to get users with night stay
def get_by_night_stay():
    licr.execute("SELECT * FROM list WHERE night_stay==?", (1,))
    return licr.fetchall()

# Function to get users with night permission
def get_by_night_permi():
    licr.execute(
        "SELECT name,last_name,phone_number FROM list WHERE night_permi==?", (1,))
    return licr.fetchall()

# Function to get all users
def get_all_user():
    licr.execute("SELECT name,last_name,phone_number FROM list")
    return licr.fetchall()

# Function to update night permission status
def permi_night_stay(id, a):
    try:
        if get_by_id(id) is not None:
            licr.execute("UPDATE list SET night_permi=? WHERE id=?",
                         (a, id))
            liconn.commit()
    except Exception as e:
        print("error:", str(e))

# Function to update night stay status
def tonight_stay(id, a):
    try:
        if get_by_id(id) is not None:
            licr.execute("UPDATE list SET night_stay=? WHERE id=?",
                         (a, id))
            liconn.commit()
    except Exception as e:
        print("error:", str(e))

# Function to add a new user
def add_user(id, name, lastname, phonenumber):
    try:
        licr.execute("INSERT INTO list VALUES(?,?,?,?,?,?)",
                     (id, name, lastname, phonenumber, 0, 0))
        liconn.commit()
    except:
        print("error")

# Function to change user data
def change_user_data(id, name, lastname, phonenumber):
    try:
        if get_by_id(id) is not None:
            licr.execute("UPDATE list SET name=?,last_name=?,phone_number=? WHERE id=?",
                         (name, lastname, phonenumber, id,))
            liconn.commit()
    except Exception as e:
        print("error:", str(e))

# Function to reset night stay list
def reset_list():
    try:
        licr.execute("UPDATE list SET night_stay=0")
        liconn.commit()
    except Exception as e:
        print("error:", str(e))
