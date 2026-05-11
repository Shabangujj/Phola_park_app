import sys
path = '/home/shabanguj/phola_park_app'

if path not in sys.path:
    sys.path.append(path)

from phola_park_app import create_app 

application = create_app()