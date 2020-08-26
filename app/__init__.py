"""
scharlauturkey.com web project

under custom license. do not use it for commercial or public usage.

"""

from flask import Flask, current_app, g, redirect, request, url_for
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate, MigrateCommand

from config import Config

db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
babel = Babel()
csrf = CSRFProtect()
migrate = Migrate()


def create_app(config_class=Config):
    """ Initialises the Flask app """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # blueprintler buraya gelecek her blueprintden önce blueprint import edilecek hepsi yukarıda import edilmeyecek
    from app.web import bp as main_bp
    app.register_blueprint(main_bp)

    from app.search import bp as search_bp
    app.register_blueprint(search_bp)

    @app.route('/')
    def home():
        # g.lang_code = request.accept_languages.best_match(current_app.config['LANGUAGES'])
        g.lang_code = request.accept_languages.best_match(["en"])
        return redirect(url_for('web.index', lang_code="en"))

    return app

    # belki birşeyler yazabilirim


@babel.localeselector
def get_locale():
    """ Babel locale selector function """
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return g.lang_code
