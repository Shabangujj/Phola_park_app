from phola_park_app import create_app
from phola_park_app.extensions import db
from phola_park_app.model import User, UserRole

app = create_app()

with app.app_context():

    # Create roles
    roles = ["admin", "supervisor", "user"]

    for role_name in roles:
        if not UserRole.query.filter_by(name=role_name).first():
            db.session.add(UserRole(name=role_name))

    db.session.commit()

    admin_role = UserRole.query.filter_by(name="admin").first()

    # Create admin
    if not User.query.filter_by(email="admin@pholapark.co.za").first():
        admin = User(
            username="admin",
            email="admin@pholapark.co.za",
            role_id=admin_role.id
        )
        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin user created")
    else:
        print("Admin already exists")
