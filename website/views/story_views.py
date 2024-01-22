from flask import Blueprint, render_template, redirect, current_app
from get_data import buildStoryQueue
import flask_login

story_views = Blueprint('views', __name__)
new_stories_queue = None
top_stories_queue = None
best_stories_queue = None
current_story = None

@story_views.route('/new')
def newStories():
    global new_stories_queue
    if new_stories_queue is None:
        new_stories_queue = buildStoryQueue("newstories")
    current_story = next(new_stories_queue)

    html_file_variables = {}
    print(type(current_app.config))
    html_file_variables["base_file"] = current_app.config['base_template']
    html_file_variables["story_title"] = current_story.title
    html_file_variables["story_snapshot"] = current_story.snapshot
    html_file_variables["story_link"] = current_story.link
    html_file_variables["refresh_link"] = 'new'
    html_file_variables["save_link"] = 'save_story?id={0}'.format( str(current_story.hacker_news_id) )
    html_file_variables["anonymous"] = flask_login.current_user.is_anonymous

    return render_template('story_view.html', **html_file_variables)

@story_views.route('/top')
@flask_login.login_required
def topStories():
    global top_stories_queue
    if top_stories_queue is None:
        top_stories_queue = buildStoryQueue("topstories")
    current_story = next(top_stories_queue)

    html_file_variables = {}
    html_file_variables["base_file"]=current_app.config['base_template']
    html_file_variables["story_title"]=current_story.title
    html_file_variables["story_snapshot"]=current_story.snapshot
    html_file_variables["story_link"]=current_story.link
    html_file_variables["refresh_link"]='top'
    html_file_variables["save_link"]='save_story?id={0}'.format( str(current_story.hacker_news_id) )

    return render_template('story_view.html', **html_file_variables)