from flask import Blueprint, render_template, session, request, redirect, current_app

nav_blueprint = Blueprint('nav',__name__)

@nav_blueprint.route("/")
@nav_blueprint.route("/home")
def home():
    html_file_variables = {}

    html_file_variables["base_file"]=current_app.config['base_template']
    html_file_variables["sign_up_link"]='/signup'
    html_file_variables["sign_in_link"]='/login'
    html_file_variables["guest_access"]='/new'

    return render_template('home.html', **html_file_variables)