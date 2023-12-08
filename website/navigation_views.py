from flask import Blueprint, render_template, session, request, redirect, current_app

nav_blueprint = Blueprint('nav',__name__)

@nav_blueprint.route("/")
@nav_blueprint.route("/home")
def home():
    return render_template('home.html', base_file=current_app.config['base_template'],
                                        sign_up_link='/signup', 
                                        sign_in_link='/login', 
                                        guest_access='/new')