import os
from flask.ext.script import Manager, Server
from app import app

app.run(debug=True)
