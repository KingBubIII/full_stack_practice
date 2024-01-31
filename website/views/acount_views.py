from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import current_user
# using 'as' statement because I'll rename the database functions file later
import DB_stuff as DB
import flask_login
from classes import USER, STORY
from get_data import getStoryItem

account_blueprint = Blueprint("acc", __name__)

@account_blueprint.route('/save_story', methods=['GET', 'POST'])
@flask_login.fresh_login_required
def saveStory():
    user_id = flask_login.current_user.id
    story_id = request.args.get('id', type = str)
    
    if request.method == 'GET':
        saved_status = DB.storySavedStatus(user_id, story_id)

        if saved_status:
            return "Saved"
        else:
            return "Save"
        
    elif request.method == 'POST':
        saved_status = DB.saveStory(user_id, story_id)
        
        match saved_status:
            case -1:
                return "Already saved"
            case 1:
                return "Saved successfully"
            case 0:
                return "Not saved successfully"

# handles log in form html and log in verification
@account_blueprint.route('/login', methods=['GET', 'POST'])
async def logIn():
    html_file_variables = {}
    
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

        html_file_variables["base_file"]=current_app.config['base_template']
        html_file_variables["email"]=email

        return render_template('login.html', **html_file_variables)

# handles log in form html and log in verification
@account_blueprint.route('/signup', methods=['GET', 'POST'])
def signUp():
    html_file_variables = {}

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

        html_file_variables["base_file"] = current_app.config['base_template']
        html_file_variables["email"] = email
        html_file_variables["name"] = name

        return render_template('sign_up.html', **html_file_variables)
    
@account_blueprint.route('/account', methods=['GET', 'POST'])
@flask_login.fresh_login_required
def account():
    html_file_variables = {}
    html_file_variables["base_file"] = current_app.config['base_template']
    html_file_variables["extend"] = request.args.get('extend', default=False, type=bool)
    html_file_variables["more_count"] = request.args.get('more_count', default=0, type=int)
    
    record_count = 5
    story_ids = DB.getAllSavedStoryIDs(current_user.id, 5, html_file_variables["more_count"])
    story_objs = []
    # story_objs = [getStoryItem(story_id) for story_id in story_ids]
    for story_id in story_ids:
        try:
            story_class = getStoryItem(story_id)
            if len(story_class.snapshot) < 5:
                continue
            story_objs.append(story_class)
        except Exception as e:
            print(e)
            continue

    html_file_variables["stories"] = story_objs

    return render_template('account.html', **html_file_variables)