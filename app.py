from flask import Flask
from routes.login import login_bp
from routes.admin import admin_bp
from routes.student import student_bp
import os

app = Flask(__name__)
app.secret_key = "smart_attendance_secret"

# Register Blueprints
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)

# Ensure folders exist
for folder in ['templates', 'static', 'database']:
    if not os.path.exists(folder):
        os.makedirs(folder)

if __name__ == "__main__":
    app.run(debug=True)
