import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import redis

#init app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

#init rate limiter
app.config['RATE_LIMIT']=1
app.config['RATE_LIMIT_EXPIRE']=60

#init DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

#init reddis server
cache=redis.Redis(host='redis', port=6379, db=0)

#init flask_login
login_manager = LoginManager(app)
