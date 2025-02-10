import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sinav.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)