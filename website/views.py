from flask import Blueprint, render_template, session, request, redirect
from get_data import buildStoryQueue
import os

views = Blueprint('views', __name__)
new_stories_queue = None
top_stories_queue = None
best_stories_queue = None
current_story = None

@views.route('/new')
def newStories():
    global new_stories_queue
    if new_stories_queue is None:
        new_stories_queue = buildStoryQueue(newStories=True, topStories=False, bestStories=False)
    current_story = next(new_stories_queue)

    return render_template('story_view.html', story_title=current_story.title, story_snapshot=current_story.snapshot, story_link=current_story.link, refresh_link='new', save_link='like-story')

@views.route('/top')
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