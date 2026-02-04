from phola_park_app import create_app
from phola_park_app.extensions import db
from phola_park_app.model import User

app = create_app()

with app.app_context():

    print("🧹 Deleting all existing users...")
    User.query.delete()
    db.session.commit()

    print("👤 Creating default admin user...")
    admin = User(
        name="Admin",
        email="admin@example.com",
        role="admin"
    )
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()

    print("✅ Users created successfully!")
