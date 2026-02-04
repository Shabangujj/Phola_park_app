# phola_park_app/reset_database.py

from phola_park_app import create_app, db
from phola_park_app.model import UserRole, User
from werkzeug.security import generate_password_hash


def reset_db():
    app = create_app()

    with app.app_context():
        print("⚠️ Dropping all tables...")
        db.drop_all()

        print("📦 Creating all tables...")
        db.create_all()

        # ─────────────────────────────
        # 1️⃣ Create roles
        # ─────────────────────────────
        print("🔐 Creating roles...")
        role_names = ["admin", "supervisor", "user"]
        role_map = {}

        for name in role_names:
            role = UserRole(name=name)
            db.session.add(role)
            role_map[name] = role

        # 🔴 MUST commit so roles get IDs
        db.session.commit()

        # ─────────────────────────────
        # 2️⃣ Verify admin role exists
        # ─────────────────────────────
        admin_role = role_map.get("admin") or UserRole.query.filter_by(name="admin").first()
        if not admin_role:
            raise RuntimeError("❌ Admin role was not created!")

        # ─────────────────────────────
        # 3️⃣ Create default admin user
        # ─────────────────────────────
        print("👤 Creating default admin user...")

        admin = User(
            name="System Admin",
            email="admin@pholapark.co.za",
            password_hash=generate_password_hash("admin123"),
            role=admin_role,     # ✅ relationship assignment
            is_active=True       # ✅ explicit (important)
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Database reset completed successfully!")
        print("➡️ Admin login: admin@pholapark.co.za / admin123")


if __name__ == "__main__":
    reset_db()
