from datetime import datetime

from sqlalchemy.exc import ProgrammingError

from app.email import send_email
from app.forms.contact import ContactForm
from app.forms.search import SearchForm
from app.web import bp
from flask import current_app, abort, request, g, render_template, jsonify
from app.models import Products, Category
from flask_babel import _
from random import randint
from app import db
from app.forms.quotation import QuotationForm
from app.web.countries_list import countries
import string


@bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")


@bp.before_request
def before_request():
    if g.lang_code not in current_app.config["LANGUAGES"]:
        abort(404)
    dfl = request.url_rule.defaults
    if "lang_code" in dfl:
        if dfl["lang_code"] != request.full_path.split("/")[1]:
            abort(404)


@bp.after_request
def change_headers(response):
    response.headers["Server"] = "Python"
    response.headers["Content-Security-Policy"] = "font-src 'self' data:"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.set_cookie("username", "flask", secure=True, httponly=True, samesite="Lax")
    return response


@bp.route("/index", methods=["GET"])
@bp.route("/", methods=["GET"])
def index():
    title = _("Scharlau Turkey")

    return render_template("index.jinja2", title=title)


@bp.route("/search", methods=["GET"], defaults={"lang_code": "en"})
@bp.route("/arama", methods=["GET"], defaults={"lang_code": "tr"})
def search():
    # try:

    query_value = "*" + str(request.args.get('q')) + "*"
    # girdi = girdi.replace(" ", "*")

    query_value = query_value.replace("-", "_").replace("*", "").replace(" ", "+")

    if query_value.endswith("+"):
        query_value = query_value.replace("+", "")

    query_value_clean = request.args.get('q')

    limit = 18
    page = request.args.get('page')

    if page is None:
        page = 1

    page = int(page)

    if page == 0:
        offset = 0
    elif page == 1:
        offset = 0
    elif page >= 2:
        offset = (page - 1) * limit

    next_page = page + 1
    prev_page = page - 1
    limit = str(limit)
    offset = str(offset)

    query = db.engine.execute("SELECT name, model, cas_number, url, MATCH (chemical_name, model) "
                              "AGAINST ('" + query_value + "') AS relevance FROM products WHERE MATCH(chemical_name,name,"
                                                           "model,cas_number,description,search_meta,merck_equiv) AGAINST('+" + query_value +
                              "*' IN BOOLEAN MODE) ORDER BY relevance DESC LIMIT " + limit + " OFFSET " + offset + ";")

    d, a = {}, []

    for rowproxy in query:
        for column, value in rowproxy.items():

            if type(value) == str:
                if "_" in value:
                    value = value.replace("_", "-")

            d = {**d, **{column: value}}
        a.append(d)

    query_sayfa_adedi = len(a)

    return render_template("search_template.jinja2", query_value_clean=query_value_clean, limit=int(limit), products=a,
                           products_count=query_sayfa_adedi, page=page,
                           next_page=next_page, prev_page=prev_page, query_value=query_value, offset=int(offset))

    # return render_template("search_template.jinja2")

    # except ProgrammingError:

    #     return abort(404)


@bp.route("/contact", methods=['GET', 'POST'], defaults={"lang_code": "en"})
@bp.route("/iletisim", methods=['GET', 'POST'], defaults={"lang_code": "tr"})
def contact():
    form = ContactForm()
    form.country.choices = [(i['code'], i['name']) for i in countries]

    if request.method == "GET":
        return render_template("contact.jinja2", form=form)

    if request.method == "POST":
        subject = "CONTACT REQUEST"
        sender = current_app.config['MAIL_USERNAME']
        recipients_visisor = [form.email.data]
        recipients_personnel = ["webmaster@analitikkimya.com.tr"]
        text_body = render_template("contact_mail.txt", form=form)
        html_body = render_template("contact_mail.jinja2", form=form)
        # send email to customer
        send_email(subject, sender, recipients_visisor, text_body, html_body)
        # send email to personnel
        send_email(subject, sender, recipients_personnel, text_body, html_body)

        return jsonify(status="success", name=form.name_surname.data)


@bp.route("/urun/<url>", methods=["GET", "POST"], defaults={"lang_code": "tr"})
@bp.route("/product/<url>", methods=["GET", "POST"], defaults={"lang_code": "en"})
def product(url):
    product = Products.query.filter_by(url=url).first()
    form = QuotationForm()

    form.product_sku.choices = [(x.sku, x.sku) for x in product.packing]

    form.country.choices = [(i['code'], i['name']) for i in countries]

    if request.method == "GET":

        images = []

        for image in product.packing:
            if "chemical" in image.image:
                image1 = image.image.split("\n")
                images += image1
            else:
                image1 = image.image.split("\n")
                images += image1
        if len(images) == 0:
            images = "hl_logo_scharlau_168.jpg"
        elif len(images) > 0:
            images = images[0]

        product.name = product.name.replace("_", "-")
        if product.chemical_name:
            product.chemical_name = product.chemical_name.replace("_", "-")

        return render_template("product.jinja2", product=product, image=images, form=form)

    if request.method == "POST":

        if not form.validate_on_submit():

            return jsonify(form.errors)

        else:
            subject = "QUOTATION REQUEST FOR " + form.product_name.data
            sender = current_app.config['MAIL_USERNAME']
            recipients_visisor = [form.email.data]
            recipients_personnel = ["webmaster@analitikkimya.com.tr"]
            text_body = render_template("quotation_mail.txt", form=form)
            html_body = render_template("quotation_mail.jinja2", form=form)
            # send email to customer
            send_email(subject, sender, recipients_visisor, text_body, html_body)
            # send email to personnel
            send_email(subject, sender, recipients_personnel, text_body, html_body)
            return jsonify(status="success", name=form.name_surname.data)


@bp.route("/kimyasallar", methods=["GET"], defaults={"lang_code": "tr"})
@bp.route("/chemicals", methods=["GET"], defaults={"lang_code": "en"})
def chemicals():
    page = request.args.get('page', 1)
    page = int(page)
    next_page = page + 1
    prev_page = page - 1
    limit = 18
    if page == 1:
        offset = 0
    elif page >= 2:
        offset = (page - 1) * limit

    letter = request.args.get("letter", None)

    products = Products.query.order_by(Products.name).offset(offset).limit(limit)
    products_count = products.count()

    product_filtered = list()

    letter_set = set()

    products_all = Products.query.all()

    for letter_f in string.ascii_uppercase:
        for product in products_all:
            if product.name.upper().startswith(letter_f):
                letter_set.add(letter_f)

    letters_sorted = sorted(letter_set)

    if letter is not None:
        if letter != "0..9":
            for product in products_all:
                if product.name.upper().startswith(letter):
                    product_filtered.append(product)
        elif letter == "0..9":
            for product in products_all:
                for i in range(0, 9):
                    if product.name.startswith(str(i)):
                        product_filtered.append(product)

        products = product_filtered[offset:offset + limit]
        products_count = len(products)

    for product in products:
        if product.name:
            product.name = product.name.replace("_", "-")

        if product.cas_number:
            product.cas_number = product.cas_number.replace("_", "-")

        if product.chemical_name:
            product.chemical_name = product.chemical_name.replace("_", "-")

        if product.description is None:
            product.description = ""

        if product.cas_number is None:
            product.cas_number = "Not Available"

    return render_template("chemicals.jinja2", products=products, page=page,
                           next_page=next_page, prev_page=prev_page, products_count=products_count, limit=limit,
                           letter=letter, letters=letters_sorted)


@bp.route("/farma", methods=["GET"], defaults={"lang_code": "tr"})
@bp.route("/pharma", methods=["GET"], defaults={"lang_code": "en"})
def pharma():
    page = request.args.get('page')
    if page is None:
        page = 1
    page = int(page)
    next_page = page + 1
    prev_page = page - 1
    limit = 18
    if page == 1:
        offset = 0
    elif page >= 2:
        offset = (page - 1) * limit

    products = Products.query.order_by(Products.name).filter(Products.name.ilike("%Pharmpur%")).offset(offset).limit(limit)
    products_count = products.count()

    letter = request.args.get("letter", None)

    product_filtered = list()

    letter_set = set()

    products_all = Products.query.order_by(Products.name).filter(Products.name.ilike("%Pharmpur%"))

    for letter_f in string.ascii_uppercase:
        for product in products_all:
            if product.name.upper().startswith(letter_f):
                letter_set.add(letter_f)

    letters_sorted = sorted(letter_set)

    if letter is not None:
        if letter != "0..9":
            for product in products_all:
                if product.name.upper().startswith(letter):
                    product_filtered.append(product)
        elif letter == "0..9":
            for product in products_all:
                for i in range(0, 9):
                    if product.name.startswith(str(i)):
                        product_filtered.append(product)

        products = product_filtered[offset:offset + limit]
        products_count = len(products)

    for product in products:
        if product.name:
            product.name = product.name.replace("_", "-")

        if product.cas_number:
            product.cas_number = product.cas_number.replace("_", "-")

        if product.chemical_name:
            product.chemical_name = product.chemical_name.replace("_", "-")

        if product.description is None:
            product.description = ""

        if product.cas_number is None:
            product.cas_number = "Not Available"

    return render_template('pharma.jinja2', products=products, page=page,
                           next_page=next_page, prev_page=prev_page, products_count=products_count, limit=limit, letters=letters_sorted, letter=letter)


@bp.route("/kozmetik", methods=["GET"], defaults={"lang_code": "tr"})
@bp.route("/cosmetics", methods=["GET"], defaults={"lang_code": "en"})
def cosmetics():
    page = request.args.get('page')
    if page is None:
        page = 1
    page = int(page)
    next_page = page + 1
    prev_page = page - 1
    limit = 18
    if page == 1:
        offset = 0
    elif page >= 2:
        offset = (page - 1) * limit

    products = Products.query.order_by(Products.name).filter_by(category_id=53).offset(offset).limit(limit)
    products_count = products.count()

    letter = request.args.get("letter", None)

    product_filtered = list()

    letter_set = set()

    products_all = Products.query.order_by(Products.name).filter_by(category_id=53)

    for letter_f in string.ascii_uppercase:
        for product in products_all:
            if product.name.upper().startswith(letter_f):
                letter_set.add(letter_f)

    letters_sorted = sorted(letter_set)

    if letter is not None:
        if letter != "0..9":
            for product in products_all:
                if product.name.upper().startswith(letter):
                    product_filtered.append(product)
        elif letter == "0..9":
            for product in products_all:
                for i in range(0, 9):
                    if product.name.startswith(str(i)):
                        product_filtered.append(product)

        products = product_filtered[offset:offset + limit]
        products_count = len(products)

    for product in products:
        if product.name:
            product.name = product.name.replace("_", "-")
        if product.cas_number:
            product.cas_number = product.cas_number.replace("_", "-")
        if product.chemical_name:
            product.chemical_name = product.chemical_name.replace("_", "-")

    return render_template('cosmetics.jinja2', products=products, page=page,
                           next_page=next_page, prev_page=prev_page, products_count=products_count, limit=limit, letter=letter, letters=letters_sorted)


@bp.route("/mikrobiyoloji", methods=["GET"], defaults={"lang_code": "tr"})
@bp.route("/microbiology", methods=["GET"], defaults={"lang_code": "en"})
def microbiology():
    page = request.args.get('page')
    if page is None:
        page = 1
    page = int(page)
    next_page = page + 1
    prev_page = page - 1
    limit = 18
    if page == 1:
        offset = 0
    elif page >= 2:
        offset = (page - 1) * limit

    products = Products.query.order_by(Products.name).filter_by(category_id=36).offset(offset).limit(limit)
    products_count = products.count()

    letter = request.args.get("letter", None)

    product_filtered = list()
    product_filtered_num = list()

    letter_set = set()

    products_all = Products.query.order_by(Products.name).filter_by(category_id=36)

    for letter_f in string.ascii_uppercase:
        for product in products_all:
            if product.name.upper().startswith(letter_f):
                letter_set.add(letter_f)

    letters_sorted = sorted(letter_set)

    if letter is not None:
        if letter != "0..9":
            for product in products_all:
                if product.name.upper().startswith(letter):
                    product_filtered.append(product)
        elif letter == "0..9":
            for product in products_all:
                for i in range(0, 9):
                    if product.name.startswith(str(i)):
                        product_filtered.append(product)

        products = product_filtered[offset:offset + limit]
        products_count = len(products)

    for product in products:
        if product.name:
            product.name = product.name.replace("_", "-")

        if product.cas_number:
            product.cas_number = product.cas_number.replace("_", "-")

        if product.chemical_name:
            product.chemical_name = product.chemical_name.replace("_", "-")

        if product.description is None:
            product.description = ""

        if product.cas_number is None:
            product.cas_number = "Not Available"

    return render_template('microbiology.jinja2', products=products, page=page,
                           next_page=next_page, prev_page=prev_page, products_count=products_count, limit=limit, letter=letter, letters=letters_sorted)


@bp.route("/dokumantasyon", methods=["GET", "POST"], defaults={"lang_code": "tr"})
@bp.route("/documentation", methods=["GET", "POST"], defaults={"lang_code": "en"})
def documentation():
    return render_template("documentation.jinja2")


@bp.context_processor
def context_process():
    random_int = randint(1, 1847)
    random_p_query = db.engine.execute("SELECT chemical_name FROM products WHERE product_id = " + str(random_int))
    return dict(random_product=random_p_query.fetchall()[0][0].replace("_", "-"), now=datetime.utcnow())
