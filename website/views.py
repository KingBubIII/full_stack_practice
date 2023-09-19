from flask import Blueprint, render_template, session
from get_data import buildStoryQueue

views = Blueprint('views', __name__)
queue = buildStoryQueue()

@views.route('/')
def viewStory():
    var = next(queue)
    return render_template('story_view.html', story_title=var.title, story_snapshot=var.snapshot, story_link=var.link)