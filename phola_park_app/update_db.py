# phola_park_app/update_db.py
from phola_park_app import create_app
from phola_park_app.extensions import db

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Tables created (db.create_all())")

if __name__ == "__main__":
    main()
