import pandas as pd
import sqlite3

def export_to_excel():
    conn = sqlite3.connect("database/attendance.db")
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    df.to_excel("Attendance_Report.xlsx", index=False)
