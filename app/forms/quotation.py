from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_babel import lazy_gettext as _l


class QuotationForm(FlaskForm):
    email = EmailField(_l('Email'), validators=[DataRequired()])
    company = StringField(_l('Company Name'), validators=[DataRequired()])
    phone = TelField(_l('Phone Number'), validators=[DataRequired()])
    name_surname = StringField(_l('Name-Surname'), validators=[DataRequired()])
    country = SelectField(_l('Country'), validators=[DataRequired()])
    message = TextAreaField(_l('Quotation Details'), validators=[DataRequired()])
    product_name = StringField()
    product_sku = SelectField(_l("Product Packing"), validators=[DataRequired()])
    qty = StringField(_l('Quantity you need to get quoted for'), validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField(_l('Submit Quotation Request'))
