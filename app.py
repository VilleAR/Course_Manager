from flask import Flask
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import MultiDict


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
import routes


