from flask import Flask
from InstagramTracker import config
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mongoengine import MongoEngine




app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret_key
app.config['MONGODB_SETTINGS'] = {
    'db': config.mongo_db,
    'host': config.mongo_uri
}
db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"
login_manager.login_message_category = "info"
# mongo = PyMongo(app)
bcrypt = Bcrypt(app)

from InstagramTracker import routes
