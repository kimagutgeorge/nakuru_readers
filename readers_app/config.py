import os
from flask import Flask, request,jsonify,json, session
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import or_
from flask import url_for
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
# app.config['UPLOAD_FOLDER'] = '../front/src/assets/images/bg/events'
# app.config['BLOG_FOLDER'] = '../front/src/assets/images/bg/blogs'
# app.config['UPLOAD_PRODUCT'] = '../front/src/assets/images/bg/products'
# app.config['MEMBER_FOLDER'] = '../front/src/assets/images/bg/members'

# email
# smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
# smtp_port = 587  # Replace with your SMTP port
# password = "fqcy btct skpv wlxx"
# sender_email = "yako.mailer@gmail.com"

# secret key
app.secret_key = 'ae68177cfc47043d80d622007229de84348c9c43d36350e5b36366ddf308c454'

db = SQLAlchemy(app)

# Allowed extensions for validation
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# Allow CORS for requests from vue
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)

# integer checker
def is_integer(valuetoCheck):
    try:
        int(valuetoCheck)
    except ValueError:
        return False
    else:
        return True