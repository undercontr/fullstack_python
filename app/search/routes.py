from sqlalchemy.exc import ProgrammingError

from app.search import bp
from flask import jsonify, request
from app import db


@bp.route("/get_search_data", methods=["POST"])
def get_search_data():
    girdi = request.form['searchbox']

    girdi = girdi.replace("-", "_").replace("*", "").replace(" ", "+")

    if girdi.endswith("+"):
        girdi = girdi.replace("+", "")

    query = db.engine.execute("SELECT name, model, cas_number, url, MATCH (chemical_name, model) "
                              "AGAINST ('" + girdi + "') AS relevance FROM products WHERE MATCH(chemical_name,name,"
                                                     "model,cas_number,description,search_meta,merck_equiv) AGAINST('+" + girdi +
                              "*' IN BOOLEAN MODE) ORDER BY relevance DESC LIMIT 8;")

    d, a = {}, []

    for rowproxy in query:
        for column, value in rowproxy.items():

            if type(value) == str:
                value = value.replace("_", "-")

            d = {**d, **{column: value}}

        a.append(d)

    return jsonify(a)


@bp.route("/get_docs_data", methods=["POST"])
def get_docs_data():
    girdi = request.form['docbox']

    girdi = girdi.replace("*", "").replace(" ", "+")

    if girdi.endswith("+"):
        girdi = girdi.replace("+", "")

    query = db.engine.execute("SELECT name, model, url, msds, tds, MATCH (model) "
                              "AGAINST ('" + girdi + "') AS relevance FROM products WHERE MATCH(model) AGAINST('+" + girdi +
                              "*' IN BOOLEAN MODE) ORDER BY relevance DESC LIMIT 8;")

    d, a = {}, []

    for rowproxy in query:
        for column, value in rowproxy.items():

            d = {**d, **{column: value}}

        a.append(d)

    return jsonify(a)
