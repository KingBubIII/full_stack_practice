from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET _KEY'] = 'asdf'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
