from app import create_app, db, translate, scss
from app.models import Products, SubCategory, Category

app = create_app()

translate.register(app)
scss.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Products': Products, 'SubCategory': SubCategory, 'Category': Category}
