from flask import Blueprint, render_template, session, request, redirect, current_app
from get_data import buildStoryQueue
# using 'as' statement because I'll rename the database functions file later
import DB_stuff as DB
import flask_login
from classes import USER

account_blueprint = Blueprint("acc", __name__)

@account_blueprint.route('/like-story')
def saveStory():
    feed = request.args.get('feed', type = str)
    print(feed)
    return redirect("/{0}".format(feed))

# handles log in form html and log in verification
@account_blueprint.route('/login', methods=['GET', 'POST'])
async def logIn():
    # if the form is submitted via button
    if request.method == 'POST':
        current_user = USER( (request.form['email'], request.form['password']) )

        if current_user.successful:
            flask_login.login_user(current_user)
            current_app.config['base_template'] = "signed_in_base.html"
            # default to new story queue
            return redirect('/new')
        else:
            # reloads html with user typed email being pretyped
            return redirect('/login?email={0}'.format(request.form['email']))
    else:
        # setting a default value from last form submission
        if len(request.args.keys()) == 0:
            email = ''
        else:
            email = request.args.get('email', type = str)

        return render_template('login.html', base_file=current_app.config['base_template'],
                                            email=email)

# handles log in form html and log in verification
@account_blueprint.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        result = DB.signUp(request.form)
        if result:
            return redirect('/login')
        else:
            # reloads html with prefilled in data excluding the passwords
            return redirect('/signup?email={0}&name={1}'.format(email, name))
    else:
        # setting a default value from last form submission
        if len(request.args.keys()) == 0:
            email = ''
            name = ''
        else:
            email = request.args.get('email', type = str)
            name = request.args.get('name', type = str)

        return render_template('sign_up.html', base_file=current_app.config['base_template'],
                                                email=email, 
                                                name=name)