import os
from dotenv import load_dotenv

root_directory = os.path.abspath(os.path.dirname(__name__))

load_dotenv(os.path.join(root_directory, '.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.environ.get('SECRET_KEY')