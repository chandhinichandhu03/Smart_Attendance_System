import sqlite3
conn = sqlite3.connect('database/attendance.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll_no TEXT UNIQUE,
    department TEXT,
    mobile TEXT,
    password TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    date TEXT,
    status TEXT
)""")

cur.execute("INSERT OR IGNORE INTO admin (email, password) VALUES ('admin@gmail.com', 'admin123')")
conn.commit()
conn.close()
print("✅ Database initialized successfully!")
