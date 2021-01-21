"""Payment Processing API for Filed.com application."""

from flask import Flask
from flask import app

from app.routes.payment import payment_bp


app = Flask(__name__)
app.register_blueprint(payment_bp)
