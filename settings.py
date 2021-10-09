from flask import Flask
from flask_restful import  Api

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ChallengeSnoop.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 