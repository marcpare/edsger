import os
import bottle
import app

os.chdir(os.path.dirname(__file__))

application = bottle.default_app()
