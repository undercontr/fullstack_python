import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'd73626094f1e438e8ec5b07128e71899'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://test:test@localhost:3306/testdeneme_scharlau'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
