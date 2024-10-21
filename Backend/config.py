# config.py
import os
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

class Config:
    FIREBASE_SERVICE_ACCOUNT_KEY = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY')
    secret_key_bytes = os.urandom(32)

# Convert the bytes to a string
    secret_key = secret_key_bytes.hex()

# Set the secret key on the Flask app
    app.secret_key = secret_key
    CORS(app)
    
