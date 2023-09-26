from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')
    app.secret_key = "GROCERY PROJECT"

    from . import order
    from . import user
    from . import supplier
    from . import product

    app.register_blueprint(user.user_bp)
    app.register_blueprint(order.order_bp)
    app.register_blueprint(supplier.supplier_bp)
    app.register_blueprint(product.product_bp)

    from main.db import close_db

    @app.teardown_appcontext
    def teardown_appcontext(error):
        close_db(error)

    @app.route('/')
    def hello():
        return render_template('welcome.html')

    return app
