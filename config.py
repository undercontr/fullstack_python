import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'd73626094f1e438e8ec5b07128e71899'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://test:test@localhost:3306/testdeneme_scharlau'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "webmaster@analitikkimya.com.tr"
    MAIL_PASSWORD = "Anw6318A."
    MAIL_DEBUG = False
    ADMINS = ['webmaster@analitikkimya.com.tr']
    LANGUAGES = ['en', 'tr']
    DATA_PER_PAGE = 25
    RECAPTCHA_PUBLIC_KEY = "6Lf7OVcUAAAAAGiFguM0f62nkEiBGT_trydb5DM2"
    RECAPTCHA_PRIVATE_KEY = "6Lf7OVcUAAAAAIw-7pk5A5F3VdeGoGzU45KnM56E"
