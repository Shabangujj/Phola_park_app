from phola_park_app.extensions import create_app, db
from phola_park_app.model import User, UserRole
from werkzeug.security import generate_password_hash

def seed_users():
    app = create_app()

    with app.app_context():
        admin_role = UserRole.query.filter_by(name="admin").first()
        supervisor_role = UserRole.query.filter_by(name="supervisor").first()
        user_role = UserRole.query.filter_by(name="user").first()

        users = [
            {
                "name": "Admin User",
                "email": "admin@test.com",
                "password": "adminpass",
                "role": admin_role
            },
            {
                "name": "Supervisor User",
                "email": "supervisor@test.com",
                "password": "supervisorpass",
                "role": supervisor_role
            },
            {
                "name": "Normal User",
                "email": "user@test.com",
                "password": "userpass",
                "role": user_role
            },
        ]

        for data in users:
            existing = User.query.filter_by(email=data["email"]).first()

            if existing:
                print(f"✔ {data['email']} already exists — skipping")
                continue

            user = User(
                name=data["name"],
                email=data["email"],
                password_hash=generate_password_hash(data["password"]),
                role=data["role"],
            )

            db.session.add(user)
            print(f"➕ Created {data['email']}")

        db.session.commit()
        print("✅ User seeding completed successfully")

if __name__ == "__main__":
    seed_users()
