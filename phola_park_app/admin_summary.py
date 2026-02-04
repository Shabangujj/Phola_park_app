# admin_summary.py
import os
from datetime import datetime
from collections import Counter

# Paths
DB_FOLDER = r"C:\Users\SHABANGU\Downloads\phola_park_app_v1"
LOG_FILE = os.path.join(DB_FOLDER, "admin_tools_log.txt")

def parse_logs():
    """Read and parse the admin_tools_log.txt file."""
    if not os.path.exists(LOG_FILE):
        print("⚠️  No log file found. Run admin_tools.py at least once.")
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as log:
        lines = log.readlines()

    logs = []
    for line in lines:
        try:
            # Example line: [2025-11-09 23:25:16] [OK] Test Connection - 5 tables found.
            timestamp = line[1:20]
            status = line.split("] [")[1].split("]")[0]
            rest = line.split("] ")[2]
            if " - " in rest:
                action, message = rest.split(" - ", 1)
            else:
                action, message = rest, ""
            logs.append({
                "timestamp": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                "status": status.strip(),
                "action": action.strip(),
                "message": message.strip()
            })
        except Exception:
            continue
    return logs


def summarize_logs(logs):
    """Generate and display summary statistics."""
    if not logs:
        print("⚠️  No data found in log file.")
        return

    print("\n====================================")
    print("📊 PHOLA PARK ADMIN SUMMARY DASHBOARD")
    print("====================================")

    # --- Totals ---
    total_actions = len(logs)
    actions = Counter(log["action"] for log in logs)
    statuses = Counter(log["status"] for log in logs)

    print(f"\n🧾 Total Actions Logged: {total_actions}")
    print(f"🕒 Period Covered: {logs[0]['timestamp'].strftime('%Y-%m-%d')} → {logs[-1]['timestamp'].strftime('%Y-%m-%d')}")

    print("\n📦 Action Breakdown:")
    for action, count in actions.items():
        print(f"   • {action}: {count}")

    print("\n🟢 Status Breakdown:")
    for status, count in statuses.items():
        icon = "✅" if status == "OK" else "⚠️" if status == "WARN" else "❌" if status == "ERROR" else "ℹ️"
        print(f"   {icon} {status}: {count}")

    # --- Most Recent Logs ---
    print("\n🕓 10 Most Recent Actions:")
    recent = logs[-10:]
    for entry in recent:
        print(f"   [{entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}] {entry['status']:>5} | {entry['action']} - {entry['message']}")

    print("\n====================================")
    print("✅ Summary generated successfully.\n")


def export_csv(logs):
    """Export the logs to CSV for reporting."""
    if not logs:
        print("⚠️  Nothing to export.")
        return

    export_file = os.path.join(DB_FOLDER, "admin_tools_report.csv")
    with open(export_file, "w", encoding="utf-8") as f:
        f.write("Timestamp,Status,Action,Message\n")
        for log in logs:
            f.write(f"{log['timestamp']},{log['status']},{log['action']},{log['message']}\n")

    print(f"📁 Logs exported to CSV: {export_file}")


def main():
    print("\n📊 Loading Phola Park Admin Summary...\n")
    logs = parse_logs()
    summarize_logs(logs)

    choice = input("Would you like to export this summary to CSV? (y/n): ").strip().lower()
    if choice == "y":
        export_csv(logs)
    else:
        print("✅ Summary complete. No export created.")


if __name__ == "__main__":
    main()
