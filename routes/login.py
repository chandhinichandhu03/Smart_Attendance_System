from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3

login_bp = Blueprint('login', __name__)

DB = "database/attendance.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        if role == 'admin':
            cur.execute("SELECT * FROM admin WHERE email=? AND password=?", (username, password))
            admin = cur.fetchone()
            if admin:
                session['admin'] = admin['email']
                return redirect(url_for('admin.dashboard'))
        else:
            cur.execute("SELECT * FROM students WHERE roll_no=? AND password=?", (username, password))
            student = cur.fetchone()
            if student:
                session['student'] = student['roll_no']
                return redirect(url_for('student.dashboard'))

        flash("Invalid credentials. Try again!")
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))
