from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from service.hasher import make_hash_from, are_strings_same

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Mypassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)