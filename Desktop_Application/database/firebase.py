import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("database/serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://biometric-attendance-sys-2b494-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

students_db = db.reference("students")
attendance_db = db.reference("attendance")
reports_db = db.reference("reports")
settings_db = db.reference("settings")