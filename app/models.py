from slugify import slugify

from app import db, create_app


utf8 = "utf8_general_ci"


class Products(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey("subcategory.subcategory_id"))
    name = db.Column(db.String(2 ** 11, utf8), nullable=False)
    model = db.Column(db.String(2 ** 11, utf8), nullable=False)
    cas_number = db.Column(db.String(2*11, utf8), nullable=True)
    chemical_name = db.Column(db.Text(2**15, utf8), nullable=True)
    description = db.Column(db.Text(2 ** 15, utf8))
    msds = db.Column(db.String(2**11, utf8))
    tds = db.Column(db.String(2 ** 11, utf8))
    merck_equiv = db.Column(db.String(2 ** 11, utf8))
    url = db.Column(db.String(2 ** 11, utf8), unique=True)
    search_meta = db.Column(db.String(2 ** 11, utf8))

    packing = db.relationship("ProductPacking")
    specification = db.relationship("Specification")
    category = db.relationship("SubCategory")

    # def __init__(self, name, model, description, category_id, url, search_meta):
    #     self.name = name
    #     self.model = model
    #     self.description = description
    #     self.category_id = category_id
    #     self.url = slugify(url)
    #     self.search_meta = search_meta


class ProductPacking(db.Model):

    __tablename__ = "product_packing"

    product_packing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    packing_id = db.Column(db.Integer, db.ForeignKey("packing_definitions.packingdef_id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id", ))
    sku = db.Column(db.String(2 ** 10, utf8))
    image = db.Column(db.String(2 ** 11, utf8))

    packing_value = db.relationship("PackingDefinitions")

    # def __init__(self, packing_id, sku, packing, product_id):
    #     self.packing_id = packing_id
    #     self.sku = sku
    #     self.packing = packing
    #     self.product_id = product_id


class PackingDefinitions(db.Model):

    __tablename__ = "packing_definitions"

    packingdef_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2**11, utf8), nullable=False)

    def __init__(self, packing_value):
        self.packing_value = packing_value


class Specification(db.Model):

    __tablename__ = "specification"

    specification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id", ))
    spec_value_id = db.Column(db.Integer, db.ForeignKey("specification_definitions.specificationdef_id"))
    value = db.Column(db.Text(collation=utf8), nullable=False)

    spec_def = db.relationship("SpecificationDefinitions")


class SpecificationDefinitions(db.Model):

    __tablename__ = "specification_definitions"

    specificationdef_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2**11, utf8), nullable=False)


class SubCategory(db.Model):
    __tablename__ = "subcategory"

    subcategory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    name = db.Column(db.String(2 ** 11, utf8), nullable=False)
    url = db.Column(db.String(2 ** 11, utf8), nullable=False)

    procucts = db.relationship("Products")
    category = db.relationship("Category")

    # def __init__(self, subcategory_id, name, url, category_id):
    #     self.subcategory_id = subcategory_id
    #     self.name = name
    #     self.url = slugify(url)
    #     self.category_id = category_id


class Category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2 * 11, utf8), nullable=False)
    url = db.Column(db.String(2 ** 11, utf8), nullable=False)

    subcategories = db.relationship("SubCategory")

    # def __init__(self, cateory_id, name, url):
    #     self.category_id = cateory_id
    #     self.name = name
    #     self.url = slugify(url)


with create_app().app_context():

    # db.drop_all() and db.create_all() will be commented out on production.
    # db.drop_all()
    # db.create_all()
    pass