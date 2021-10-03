from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask
from frontend.app import app as frontend
from backend.app import app as backend

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(frontend, {"/api": backend})
