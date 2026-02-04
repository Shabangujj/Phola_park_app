# phola_park_app/test_connection.py
from sqlalchemy import text
from phola_park_app import create_app
from phola_park_app.extensions import db   # adjust import if your extensions module name is different

def main():
    app = create_app()
    # run inside app context so flask-sqlalchemy knows the config
    with app.app_context():
        # Using the db.engine (SQLAlchemy Engine object)
        engine = db.engine
        print("Connected to DB:", engine)
        # Use a connection object to execute SQL (SQLAlchemy v1.4+ / 2.x style)
        with engine.connect() as conn:
            # simple test query
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            print("DB Test OK:", row[0])

if __name__ == "__main__":
    main()
