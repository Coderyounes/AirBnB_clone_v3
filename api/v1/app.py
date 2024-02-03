#!/usr/bin/python3
""" Main Flask APP"""
from flask import Flask
from models import storage
from os import environ
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(err):
    """
        db close method
    """
    storage.close()


if __name__ == "__main__":
    """ Principal function """
    host = environ.get("HBNB_API_HOST")
    port = environ.get("HBNB_API_PORT")
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
