# phola_park_app/reset_database.py

from werkzeug.security import generate_password_hash

from phola_park_app import create_app
from phola_park_app.extensions import db
from phola_park_app.models import UserRole, User


def reset_db():
    app = create_app()

    with app.app_context():

        print("=" * 60)
        print("PHOLA PARK APP DATABASE RESET")
        print("=" * 60)

        print("⚠️ Dropping all tables...")
        db.drop_all()

        print("📦 Creating all tables...")
        db.create_all()

        # -----------------------------
        # Create roles
        # -----------------------------
        print("🔐 Creating roles...")

        role_names = [
            "admin",
            "supervisor",
            "user"
        ]

        role_map = {}

        for role_name in role_names:
            role = UserRole(name=role_name)
            db.session.add(role)
            role_map[role_name] = role

        db.session.commit()

        admin_role = UserRole.query.filter_by(name="admin").first()

        if admin_role is None:
            raise RuntimeError("Admin role could not be created.")

        # -----------------------------
        # Create default admin
        # -----------------------------
        print("👤 Creating default administrator...")

        admin = User.query.filter_by(
            email="admin@pholapark.co.za"
        ).first()

        if admin is None:

            admin = User(
                full_name="System Admin",
                username="admin",
                email="admin@pholapark.co.za",
                role=admin_role,
                is_active=True,
                email_verified=True,
                portfolio="administration"
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

        print()
        print("✅ Database reset completed successfully!")
        print()
        print("Default Administrator")
        print("----------------------------")
        print("Email    : admin@pholapark.co.za")
        print("Password : admin123")
        print("=" * 60)


if __name__ == "__main__":
    reset_db()