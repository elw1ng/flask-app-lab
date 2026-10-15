from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config.py")

from . import views  # noqa: E402,F401
