from flask import Flask, session
#Hello
from Database.mongodb import initialize_db, mongo
from bson import json_util
import os
# comment out below line to enable tensorflow outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Response

import socket
import threading
import time


def create_app():

    app = Flask(__name__, static_url_path='',
                static_folder='./Static',
                template_folder='./Templates')
    app.config['SECRET_KEY'] = 'my secret'

    app.config['MONGO_URI'] = ""
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
    initialize_db(app)
    

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return mongo.db.users.find_one({"email": id})

    from Routes.views import views
    from Routes.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


# <img src="{{ url_for('video_feed' , ip = cam ) }}" />
