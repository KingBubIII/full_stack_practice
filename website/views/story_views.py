from flask import Blueprint, render_template, redirect, current_app, url_for, request
from get_data import buildStoryQueue
import flask_login

story_views = Blueprint('views', __name__)
new_stories_queue = None
top_stories_queue = None
best_stories_queue = None
new_current_story = None
top_current_story = None

@story_views.route('/new')
def newStories():
    global new_stories_queue
    global new_current_story

    if new_stories_queue is None:
        new_stories_queue = buildStoryQueue("newstories")
    if new_current_story is None:
        new_current_story = next(new_stories_queue)

    html_file_variables = {}
    print(type(current_app.config))
    html_file_variables["base_file"] = current_app.config['base_template']
    html_file_variables["story_title"] = new_current_story.title
    html_file_variables["story_snapshot"] = new_current_story.snapshot
    html_file_variables["story_link"] = new_current_story.link
    html_file_variables["refresh_feed"] = 'newStories'
    html_file_variables["save_link"] = 'save_story?id={0}'.format( str(new_current_story.hacker_news_id) )
    html_file_variables["anonymous"] = flask_login.current_user.is_anonymous

    return render_template('story_view.html', **html_file_variables)

@story_views.route('/top')
@flask_login.login_required
def topStories():
    global top_stories_queue
    global top_current_story

    if top_stories_queue is None:
        top_stories_queue = buildStoryQueue("topstories")
    if top_current_story is None:
        top_current_story = next(top_stories_queue)

    html_file_variables = {}
    html_file_variables["base_file"]=current_app.config['base_template']
    html_file_variables["story_title"]=top_current_story.title
    html_file_variables["story_snapshot"]=top_current_story.snapshot
    html_file_variables["story_link"]=top_current_story.link
    html_file_variables["refresh_feed"]='topStories'
    html_file_variables["save_link"]='save_story?id={0}'.format( str(top_current_story.hacker_news_id) )

    return render_template('story_view.html', **html_file_variables)

@story_views.route('/skip')
def skip():
    feed_queue = request.args.get('feed', type = str)
    if feed_queue == 'topStories':
        global top_current_story
        top_current_story = None
    elif feed_queue == 'newStories':
        global new_current_story
        new_current_story = None

    return redirect(url_for("views.{0}".format(feed_queue)))