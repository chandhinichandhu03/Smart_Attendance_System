from flask import Blueprint, render_template, redirect, request, session, url_for, flash
import sqlite3, datetime
from utils.excel_export import export_to_excel
from utils.ai_attendance import get_low_attendance_students

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
DB = "database/attendance.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login.login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    low_attendance = get_low_attendance_students()
    return render_template('admin_dashboard.html', students=students, low_attendance=low_attendance)

@admin_bp.route('/add_student', methods=['POST'])
def add_student():
    if 'admin' not in session:
        return redirect(url_for('login.login'))
    data = (
        request.form['name'],
        request.form['roll_no'],
        request.form['department'],
        request.form['mobile'],
        request.form['password']
    )
    conn = get_db()
    conn.execute("INSERT INTO students (name, roll_no, department, mobile, password) VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    flash("Student added successfully!")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if 'admin' not in session:
        return redirect(url_for('login.login'))

    today = datetime.date.today().strftime("%Y-%m-%d")
    conn = get_db()
    cur = conn.cursor()

    for roll_no in request.form.getlist('attendance'):
        cur.execute("INSERT INTO attendance (roll_no, date, status) VALUES (?, ?, ?)", (roll_no, today, 'Present'))
    conn.commit()
    flash("Attendance marked successfully!")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/export_excel')
def export_excel():
    export_to_excel()
    flash("Attendance exported to Excel!")
    return redirect(url_for('admin.dashboard'))
