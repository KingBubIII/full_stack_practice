from flask import Blueprint, render_template, session
from get_data import buildStoryQueue

views = Blueprint('views', __name__)
new_stories_queue = buildStoryQueue(newStories=True, topStories=False, bestStories=False)
top_stories_queue = buildStoryQueue(newStories=False, topStories=True, bestStories=False)
best_stories_queue = buildStoryQueue(newStories=False, topStories=False, bestStories=True)


@views.route('/new')
def newStories():
    var = next(new_stories_queue)
    return render_template('story_view.html', story_title=var.title, story_snapshot=var.snapshot, story_link=var.link)

@views.route('/top')
def topStories():
    var = next(new_stories_queue)
    return render_template('story_view.html', story_title=var.title, story_snapshot=var.snapshot, story_link=var.link)

@views.route('/best')
def bestStories():
    var = next(new_stories_queue)
    return render_template('story_view.html', story_title=var.title, story_snapshot=var.snapshot, story_link=var.link)