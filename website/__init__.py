from flask import Flask, session
from .views.navigation_views import nav_blueprint
from .views.acount_views import account_blueprint
from .views.story_views import story_views

def create_app():
    app = Flask(__name__)
    app.config['SECRET _KEY'] = 'asdf'
    app.config['base_template'] = "no_account_base.html"

    app.register_blueprint(nav_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(story_views)

    @app.before_first_request
    def initialize():
        # This function will be executed once before the first request
        session.clear()
        print("Initialized the application")

    return app
