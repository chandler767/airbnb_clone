# imports app object from __init__ file in app directory
from app import *
from app.views import *
from config import HOST, PORT, DEBUG

# run app, passing settings imported from config file
if __name__ == '__main__':
	app.run(host=HOST, port=PORT, debug=DEBUG)