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
        new_stories_queue = buildStoryQueue(newStories=True, topStories=False, bestStories=False)
    current_story = next(new_stories_queue)

    return render_template('story_view.html', 
                            base_file=current_app.config['base_template'],
                            story_title=current_story.title,
                            story_snapshot=current_story.snapshot,
                            story_link=current_story.link, 
                            refresh_link='new',
                            save_link='save_story?id={0}'.format( str(current_story.hacker_news_id) )
                        )

@story_views.route('/top')
@flask_login.login_required
def topStories():
    global top_stories_queue
    if top_stories_queue is None:
        top_stories_queue = buildStoryQueue(newStories=False, topStories=True, bestStories=False)
    current_story = next(top_stories_queue)

    return render_template('story_view.html', 
                            base_file=current_app.config['base_template'],
                            story_title=current_story.title,
                            story_snapshot=current_story.snapshot,
                            story_link=current_story.link,
                            refresh_link='top',
                            save_link='save_story?id={0}'.format( str(current_story.hacker_news_id) )
                        )