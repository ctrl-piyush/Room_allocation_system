print("Starting Flask app...")
from flask import Flask, render_template, jsonify, request, redirect, send_file
import sqlite3
import pandas as pd
import io
from allocator import allocate_students
from database import init_db

app = Flask(__name__)
DB_PATH = 'data.db'
init_db(DB_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/allocate', methods=['POST'])
def allocate():
    allocate_students(DB_PATH)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.RoomID, s.StudentID, s.Name, s.Year
            FROM allocations a
            JOIN students s ON a.StudentID = s.StudentID
        """)
        rows = cur.fetchall()

        rooms = {}
        for room_id, student_id, name, year in rows:
            rooms.setdefault(room_id, []).append({
                "StudentID": student_id,
                "Name": name,
                "Year": year
            })

        student_count = len(rows)
        room_count = len(rooms)

    return jsonify({
        "status": "success",
        "message": f"Allocated {student_count} students across {room_count} rooms.",
        "rooms": rooms
    })

@app.route('/search_student')
def search_student():
    query = request.args.get("query", "").lower()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM students 
            WHERE LOWER(StudentID) LIKE ? OR LOWER(Name) LIKE ?
        """, (f'%{query}%', f'%{query}%'))
        student = cur.fetchone()
        if student:
            cur.execute("SELECT RoomID FROM allocations WHERE StudentID = ?", (student[0],))
            room = cur.fetchone()
            return jsonify({
                "Student": {
                    "StudentID": student[0],
                    "Name": student[1],
                    "Year": student[2],
                    "Department": student[3]
                },
                "RoomID": room[0] if room else "Not allocated"
            })
    return jsonify({"error": "Student not found or not allocated."})

@app.route('/view_room')
def view_room():
    room_id = request.args.get("room_id", "")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT StudentID FROM allocations WHERE RoomID = ?", (room_id,))
        student_ids = [sid[0] for sid in cur.fetchall()]

    ROWS, COLS = 7, 5
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    for idx, student_id in enumerate(student_ids):
        row = idx // COLS
        col = idx % COLS
        if row < ROWS:
            grid[row][col] = student_id

    return render_template("room_view.html", room_id=room_id, grid=grid)

@app.route("/stats")
def stats():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        total_students = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        total_rooms = cur.execute("SELECT COUNT(*) FROM rooms").fetchone()[0]
        total_alloc = cur.execute("SELECT COUNT(*) FROM allocations").fetchone()[0]
        heat_map = cur.execute("""
            SELECT RoomID, COUNT(*) as count, (
                SELECT Capacity FROM rooms WHERE RoomID = allocations.RoomID
            ) as capacity
            FROM allocations GROUP BY RoomID
        """).fetchall()

    return render_template("stats.html", total_students=total_students,
                           total_rooms=total_rooms,
                           total_alloc=total_alloc,
                           heat_map=heat_map)

@app.route("/search")
def search():
    year = request.args.get("year", "")
    dept = request.args.get("dept", "")
    query = "SELECT * FROM students WHERE 1=1"
    params = []
    if year:
        query += " AND Year = ?"
        params.append(year)
    if dept:
        query += " AND Department = ?"
        params.append(dept)

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(query, tuple(params))
        students = cur.fetchall()

    return render_template("search.html", students=students)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["csvfile"]
        if file:
            df = pd.read_csv(file)
            with sqlite3.connect(DB_PATH) as conn:
                df.to_sql("students", conn, if_exists="append", index=False)
            return redirect("/")
    return render_template("upload.html")

@app.route("/export")
def export():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("""
            SELECT a.StudentID, s.Name, s.Year, s.Department, a.RoomID
            FROM allocations a JOIN students s ON a.StudentID = s.StudentID
        """, conn)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Allocations")
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="allocations.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == '__main__':
    app.run(debug=True)
