from flask import Blueprint, render_template, session, request, redirect
from get_data import buildStoryQueue
# using 'as' statement because I'll rename the database functions file later
import DB_stuff as DB
from flask_login import login_user, login_required
from classes import USER

views = Blueprint('views', __name__)
new_stories_queue = None
top_stories_queue = None
best_stories_queue = None
current_story = None

@views.route('/home')
@views.route('/')
def home():
    return render_template('home.html', sign_up_link='/signup', sign_in_link='/login', guest_access='/new')

@views.route('/new')
def newStories():
    global new_stories_queue
    if new_stories_queue is None:
        new_stories_queue = buildStoryQueue(newStories=True, topStories=False, bestStories=False)
    current_story = next(new_stories_queue)

    return render_template('story_view.html', story_title=current_story.title, story_snapshot=current_story.snapshot, story_link=current_story.link, refresh_link='new', save_link='like-story')

@views.route('/top')
@login_required
def topStories():
    global top_stories_queue
    if top_stories_queue is None:
        top_stories_queue = buildStoryQueue(newStories=False, topStories=True, bestStories=False)
    current_story = next(top_stories_queue)

    return render_template('story_view.html', story_title=current_story.title, story_snapshot=current_story.snapshot, story_link=current_story.link, refresh_link='top', save_link='like-story')

"""
@views.route('/best', methods=['GET','POST'])
def bestStories():
    global best_stories_queue
    if best_stories_queue is None:
        best_stories_queue = buildStoryQueue(newStories=False, topStories=False, bestStories=True)
    current_story = next(best_stories_queue)

    return render_template('story_view.html', story_title=current_story.title, story_snapshot=current_story.snapshot, story_link=current_story.link, refresh_link='/best')
"""

@views.route('/like-story')
def saveStory():
    feed = request.args.get('feed', type = str)
    print(feed)
    return redirect("/{0}".format(feed))

# handles log in form html and log in verification
@views.route('/login', methods=['GET', 'POST'])
async def logIn():
    # if the form is submitted via button
    if request.method == 'POST':
        current_user = USER( (request.form['email'], request.form['password']) )

        if current_user.successful:
            login_user(current_user)
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

        return render_template('login.html', email=email)

# handles log in form html and log in verification
@views.route('/signup', methods=['GET', 'POST'])
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

        return render_template('sign_up.html', email=email, name=name)