from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
db=SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ankit135@localhost:5432/flask_database'

db.init_app(app)