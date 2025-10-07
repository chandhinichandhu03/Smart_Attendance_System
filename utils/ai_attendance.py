import sqlite3

def get_low_attendance_students(threshold=75):
    conn = sqlite3.connect("database/attendance.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT s.name, s.roll_no, 
        (SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END)*100.0/COUNT(a.date)) AS percentage
        FROM students s
        LEFT JOIN attendance a ON s.roll_no=a.roll_no
        GROUP BY s.roll_no
        HAVING percentage < ?
    """, (threshold,))
    return cur.fetchall()
