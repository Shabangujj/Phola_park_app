from phola_park_app import create_app
from phola_park_app.extensions import db
from phola_park_app.model import User, UserRole
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin_role = UserRole.query.filter_by(name="admin").first()

    if not admin_role:
        admin_role = UserRole(name="admin")
        db.session.add(admin_role)
        db.session.commit()

    admin = User.query.filter_by(email="admin@pholapark.com").first()

    if not admin:
        admin = User(
            name="System Admin",
            email="admin@pholapark.com",
            password_hash=generate_password_hash("Admin@123"),
            role_id=admin_role.id   # ✅ THIS IS THE FIX
        )
        db.session.add(admin)
    else:
        admin.password_hash = generate_password_hash("Admin@123")
        admin.role_id = admin_role

    db.session.commit()
    print("✅ Admin fixed correctly")
