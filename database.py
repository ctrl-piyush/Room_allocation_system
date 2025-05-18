
import sqlite3
import csv
import os

def init_db(db_path='data.db'):
    if os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("CREATE TABLE students (StudentID TEXT PRIMARY KEY, Name TEXT, Year TEXT, Department TEXT)")
    cur.execute("CREATE TABLE rooms (RoomID TEXT PRIMARY KEY, Building TEXT, Capacity INTEGER)")
    cur.execute("CREATE TABLE allocations (StudentID TEXT, RoomID TEXT, PRIMARY KEY (StudentID))")

    with open('students.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (row['StudentID'], row['Name'], row['Year'], row['Department']))

    with open('rooms.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO rooms VALUES (?, ?, ?)", (row['RoomID'], row['Building'], int(row['Capacity'])))

    conn.commit()
    conn.close()
