# Makes BYG a module

from flask import Flask

app = Flask(__name__, template_folder='.')
app.secret_key = 'development_key_123'  # You should change this to use environment variable

from . import auth
from . import byg