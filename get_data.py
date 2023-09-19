from requests import get
from json import loads
from bs4 import BeautifulSoup
from queue import SimpleQueue
import classes as c
import time

def buildStoryQueue():
    basic_URL = "https://hacker-news.firebaseio.com/v0/"
    suffix = ".json?print=pretty"
    top_story_ids_json = get(basic_URL+"newstories"+suffix)
    top_story_ids = loads(top_story_ids_json.content)
    story_queue = SimpleQueue()

    for story in top_story_ids:
        middle = 'item/'+str(story)
        current_story_data = loads(get(basic_URL+middle+suffix).content)
        yield c.STORY(current_story_data["url"], current_story_data["title"], current_story_data["id"])
        # story_queue.put(story_obj)

    # return story_queue

buildStoryQueue()