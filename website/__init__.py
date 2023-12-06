from flask import Flask
from .views import views

def create_app():
    app = Flask(__name__)
    app.config['SECRET _KEY'] = 'asdf'
    app.config['base_template'] = "no_account_base.html"

    app.register_blueprint(views, url_prefix='/')

    return app
