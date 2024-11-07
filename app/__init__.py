from flask import Flask
from flask_mongoengine import MongoEngine
import os 

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "host": "mongodb://localhost:27017/cattlecare_ai_db"
}


db = MongoEngine(app)

from app.models import Cow, Farm, User, HealthReport, Feed 
