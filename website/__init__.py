from flask import Flask
from .navigation_views import nav_blueprint
from .acount_views import account_blueprint
from .story_views import story_views

def create_app():
    app = Flask(__name__)
    app.config['SECRET _KEY'] = 'asdf'
    app.config['base_template'] = "no_account_base.html"

    app.register_blueprint(nav_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(story_views)

    return app
