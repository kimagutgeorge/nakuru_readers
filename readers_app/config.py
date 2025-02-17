import os
from flask import Flask, request,jsonify,json, session, url_for
from flask_cors import CORS, cross_origin
# from flask_sqlalchemy import SQLAlchemy#imports
# from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func, select, or_ , desc
from datetime import datetime
# from sqlalchemy import func
# from sqlalchemy import or_
# from flask import url_for
import random
import string
from flask_mail import Mail, Message
# SMTP configs
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from email.mime.image import MIMEImage
from PIL import Image,ImageOps
import os

app = Flask(__name__)
application = app
# Set config values before initializing db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postregress.$15/07/1998@localhost/book_club'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BOOKS_FOLDER'] = 'static/uploads/products'
app.config['USERS_FOLDER'] = 'static/uploads/profiles'
app.config['READS_FOLDER'] = 'static/uploads/reads'
app.config['COVERS_FOLDER'] = 'static/uploads/book_covers'

# email
# smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
# smtp_port = 587  # Replace with your SMTP port
# password = "fqcy btct skpv wlxx"
# sender_email = "yako.mailer@gmail.com"

# secret key
app.secret_key = 'ae68177cfc47043d80d622007229de84348c9c43d36350e5b36366ddf308c454'

db = SQLAlchemy(app)

# Allowed extensions for validation
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Allow CORS for requests from vue
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)
