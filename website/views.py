from flask import Blueprint, render_template, session
from get_data import buildStoryQueue

views = Blueprint('views', __name__)
new_stories_queue = None
top_stories_queue = None
best_stories_queue = None


@views.route('/new')
def newStories():
    global new_stories_queue
    if new_stories_queue is None:
        new_stories_queue = buildStoryQueue(newStories=True, topStories=False, bestStories=False)
    var = next(new_stories_queue)
    return render_template('story_view.html', story_title=var.title, story_snapshot=var.snapshot, story_link=var.link)

@views.route('/top')
def topStories():
    global top_stories_queue
    if top_stories_queue is None:
        top_stories_queue = buildStoryQueue(newStories=False, topStories=True, bestStories=False)
    var = next(top_stories_queue)
    return render_template('story_view.html', story_title=var.title, story_snapshot=var.snapshot, story_link=var.link)

@views.route('/best')
def bestStories():
    global best_stories_queue
    if best_stories_queue is None:
        best_stories_queue = buildStoryQueue(newStories=False, topStories=False, bestStories=True)
    var = next(best_stories_queue)
    return render_template('story_view.html', story_title=var.title, story_snapshot=var.snapshot, story_link=var.link)