from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_babel import lazy_gettext as _l


class ContactForm(FlaskForm):
    email = EmailField(_l('Email'), validators=[DataRequired()])
    company = StringField(_l('Company Name'), validators=[DataRequired()])
    name_surname = StringField(_l('Name-Surname'), validators=[DataRequired()])
    phone = StringField(_l('Phone Number'), validators=[DataRequired()])
    country = SelectField(_l('Country'), validators=[DataRequired()])
    message = TextAreaField(_l('Your Message'), validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField(_l('Submit'))

