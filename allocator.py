# allocator.py
import sqlite3
import random

def allocate_students(db_path: str = "data.db") -> None:
    """
    Allocate every student to a room until all beds are full.
    One simple rule: first-come (shuffled) / first-served.
    """

    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    # Wipe any previous allocations
    cur.execute("DELETE FROM allocations")

    # Pull data
    students = cur.execute("SELECT StudentID FROM students").fetchall()
    rooms    = cur.execute("SELECT RoomID, Capacity FROM rooms").fetchall()

    # Shuffle for randomness
    random.shuffle(students)

    # Build helper dicts
    room_cap = {room_id: cap for room_id, cap in rooms}
    room_load = {room_id: 0   for room_id, _   in rooms}

    # Round-robin through rooms, dropping a student wherever there’s a free bed
    room_cycle = list(room_cap.keys())
    pos = 0

    for (student_id,) in students:
        placed = False

        # Try each room once
        for _ in range(len(room_cycle)):
            room_id = room_cycle[pos]
            pos = (pos + 1) % len(room_cycle)

            if room_load[room_id] < room_cap[room_id]:
                cur.execute(
                    "INSERT INTO allocations (StudentID, RoomID) VALUES (?, ?)",
                    (student_id, room_id)
                )
                room_load[room_id] += 1
                placed = True
                break

        if not placed:
            # No bed left anywhere
            print(f"⚠️  No bed available for student {student_id}")
            break

    conn.commit()
    conn.close()
