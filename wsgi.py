import sys
import os

# add project root to PYTHONPATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from phola_park_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
