# admin_tools.py
import os
import shutil
import json
from datetime import datetime
from phola_park_app import create_app, db
from phola_park_app.model import Survey, SurveyQuestion, SurveyResponse, SurveyAnswer
from flask_login import current_user  # Import current_user from Flask-Login

# Configuration
DB_FOLDER = r"C:\Users\SHABANGU\Downloads\phola_park_app_v1"
DB_PATH = os.path.join(DB_FOLDER, "phola_park.db")
LOG_FILE = os.path.join(DB_FOLDER, "admin_tools_log.txt")

app = create_app()

# ---------- Logging Helper ----------

def log_action(action, status="INFO", message=""):
    """Write action logs with timestamp to admin_tools_log.txt"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{status}] {action} - {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_entry)

# ---------- Utility Functions ----------

def test_connection():
    """Test database connection and list tables."""
    print("\n🔍 Testing database connection...\n")
    with app.app_context():
        try:
            engine = db.get_engine()
            print(f"✅ Connected to: {engine.url}")
            inspector = db.inspect(engine)
            tables = inspector.get_table_names()
            if not tables:
                print("⚠️ No tables found in the database.")
                log_action("Test Connection", "WARN", "No tables found in DB.")
            else:
                print("📋 Tables in database:")
                for t in tables:
                    print(f"   • {t}")
                log_action("Test Connection", "OK", f"{len(tables)} tables found.")
        except Exception as e:
            print("❌ Database connection failed:", e)
            log_action("Test Connection", "ERROR", str(e))


def reset_database():
    """Backup and reset the database with confirmation."""
    print("\n⚙️  Reset Phola Park database tool")
    print("📁  Current database file:", DB_PATH)
    print("\n⚠️  WARNING: This will permanently delete ALL data and recreate empty tables.\n")

    confirm = input("Type YES to continue or press Enter to cancel: ")

    if confirm.strip().upper() == "YES":
        try:
            if os.path.exists(DB_PATH):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(DB_FOLDER, f"phola_park_backup_{timestamp}.db")
                shutil.copy2(DB_PATH, backup_path)
                print(f"💾 Backup created: {backup_path}")
                log_action("Database Reset", "INFO", f"Backup created at {backup_path}")
            else:
                print("⚠️ No existing database found. Proceeding to create new one.")
                log_action("Database Reset", "WARN", "No DB found. Created new one.")

            with app.app_context():
                print("🧹 Dropping all tables...")
                db.drop_all()

                print("🧱 Recreating tables...")
                db.create_all()

                print("✅ Database reset completed successfully.")
                log_action("Database Reset", "OK", "Tables dropped and recreated.")
        except Exception as e:
            print("❌ Database reset failed:", e)
            log_action("Database Reset", "ERROR", str(e))
    else:
        print("❎ Operation cancelled. Database was NOT modified.")
        log_action("Database Reset", "CANCEL", "User cancelled operation.")


def restore_database():
    """List backups and restore one."""
    print("\n🔁 Phola Park Database Restore Tool")
    print("📁 Active database file:", DB_PATH)

    backups = [f for f in os.listdir(DB_FOLDER) if f.startswith("phola_park_backup_") and f.endswith(".db")]

    if not backups:
        print("⚠️ No backup files found.")
        log_action("Database Restore", "WARN", "No backup files found.")
        return

    print("\n📦 Available backups:")
    for i, f in enumerate(backups, start=1):
        print(f"  {i}. {f}")

    try:
        choice = int(input("\nEnter the number of the backup to restore: "))
        if 1 <= choice <= len(backups):
            selected_backup = os.path.join(DB_FOLDER, backups[choice - 1])
            print(f"\n✅ Selected: {selected_backup}")

            confirm = input("Type YES to confirm restore (this will overwrite the active database): ")

            if confirm.strip().upper() == "YES":
                if os.path.exists(DB_PATH):
                    shutil.copy2(DB_PATH, DB_PATH.replace(".db", "_pre_restore.db"))
                    print("💾 Backup of current active database saved before restoring.")

                shutil.copy2(selected_backup, DB_PATH)
                print("✅ Database restored successfully.")
                log_action("Database Restore", "OK", f"Restored {selected_backup}")
            else:
                print("❎ Operation cancelled.")
                log_action("Database Restore", "CANCEL", "User cancelled restore.")
        else:
            print("❌ Invalid selection.")
            log_action("Database Restore", "ERROR", "Invalid backup selection.")
    except ValueError:
        print("❌ Invalid input.")
        log_action("Database Restore", "ERROR", "Invalid numeric input.")


def view_backup_history():
    """Display all backup files with date and size."""
    print("\n🗂️  Backup History - Phola Park Database\n")

    backups = [f for f in os.listdir(DB_FOLDER) if f.startswith("phola_park_backup_") and f.endswith(".db")]

    if not backups:
        print("⚠️ No backup files found.")
        log_action("View Backup History", "WARN", "No backups available.")
        return

    print(f"{'File Name':<45}{'Date Created':<25}{'Size (MB)':<10}")
    print("-" * 80)

    for f in sorted(backups):
        file_path = os.path.join(DB_FOLDER, f)
        stats = os.stat(file_path)
        file_time = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        size_mb = round(stats.st_size / (1024 * 1024), 2)
        print(f"{f:<45}{file_time:<25}{size_mb:<10}")

    print("-" * 80)
    print(f"Total backups: {len(backups)}")
    log_action("View Backup History", "OK", f"{len(backups)} backups listed.")


def backup_database_now():
    """Create an immediate manual backup of the active database."""
    print("\n💾 Manual Backup - Phola Park Database\n")

    if not os.path.exists(DB_PATH):
        print("❌ No active database file found at:")
        print(DB_PATH)
        log_action("Manual Backup", "ERROR", "No active DB found.")
        return

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(DB_FOLDER, f"phola_park_backup_{timestamp}.db")
        shutil.copy2(DB_PATH, backup_path)
        size_mb = round(os.stat(backup_path).st_size / (1024 * 1024), 2)
        print(f"✅ Backup created successfully!")
        print(f"📁 File: {backup_path}")
        print(f"📦 Size: {size_mb} MB")
        log_action("Manual Backup", "OK", f"Backup created at {backup_path} ({size_mb} MB)")
    except Exception as e:
        print("❌ Backup failed:", e)
        log_action("Manual Backup", "ERROR", str(e))


# ---------- Main Menu ----------

def notify_survey_submission(survey, user):
    """Notify the user about the survey submission."""
    print(f"✅ Survey '{survey.name}' submitted by user '{user.id}'.")

def main_menu():
    while True:
        print("\n====================================")
        print("🛠️  PHOLA PARK ADMIN TOOLS MENU")
        print("====================================")
        print("1️⃣  Test Database Connection")
        print("2️⃣  Reset Database (with Backup)")
        print("3️⃣  Restore Database from Backup")
        print("4️⃣  View Backup History")
        print("5️⃣  Backup Database Now (Manual)")
        print("6️⃣  Exit")
        print("====================================")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            test_connection()
        elif choice == "2":
            reset_database()
        elif choice == "3":
            restore_database()
        elif choice == "4":
            view_backup_history()
        elif choice == "5":
            backup_database_now()
        elif choice == "6":
            print("👋 Exiting Admin Tools. Goodbye!")
            log_action("Exit", "INFO", "Admin Tools closed.")
            break
        else:
            print("❌ Invalid option. Please choose 1–6.")

survey = Survey(
    name="Water Service Delivery Survey",
    topic="Water"
)

db.session.add(survey)
db.session.commit()
q1 = SurveyQuestion(
    survey_id=survey.id,
    text="How would you rate the quality of water service?",
    question_type="rating",
    order=1
)

q2 = SurveyQuestion(
    survey_id=survey.id,
    text="How often do you experience water interruptions?",
    question_type="multiple_choice",
    options=json.dumps([
        "Daily", "Weekly", "Rarely", "Never"
    ]),
    order=2
)
response = SurveyResponse(
    survey_id=survey.id,
    user_id=current_user.id
)

db.session.add(response)
db.session.commit()

db.session.add_all([q1, q2])
db.session.commit()
form_answers = {}  # Initialize form_answers as an empty dictionary
for question_id, answer in form_answers.items():
    notify_survey_submission(survey=survey, user=current_user)
    if isinstance(answer, list):
        answer = "; ".join(answer)

    db.session.add(
        SurveyAnswer(
            response_id=response.id,
            question_id=question_id,
            value=str(answer)
        )
    )

db.session.commit()
form_answers = {}  # Initialize form_answers as an empty dictionary

responses = (
    SurveyResponse.query
    .join(Survey)
    .filter(Survey.topic == current_user.portfolio)
    .all()
)

for question_id, answer in form_answers.items():
    notify_survey_submission(
    survey=survey,
    user=current_user
)

if __name__ == "__main__":
    main_menu()
