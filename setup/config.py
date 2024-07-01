import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mock_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
