from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3

student_bp = Blueprint('student', __name__, url_prefix='/student')
DB = "database/attendance.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@student_bp.route('/dashboard')
def dashboard():
    if 'student' not in session:
        return redirect(url_for('login.login'))
    roll_no = session['student']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE roll_no=?", (roll_no,))
    student = cur.fetchone()

    cur.execute("SELECT COUNT(*) as total, SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present FROM attendance WHERE roll_no=?", (roll_no,))
    stats = cur.fetchone()
    total = stats['total'] if stats['total'] else 0
    present = stats['present'] if stats['present'] else 0
    percentage = (present / total * 100) if total > 0 else 0

    cur.execute("SELECT * FROM attendance WHERE roll_no=?", (roll_no,))
    records = cur.fetchall()

    return render_template('student_dashboard.html', student=student, percentage=percentage, records=records)
