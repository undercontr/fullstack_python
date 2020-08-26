from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    q = StringField(_l("Search Form"), validators=[DataRequired()])
    submit = SubmitField(_l("Search"))
