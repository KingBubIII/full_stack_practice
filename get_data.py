from requests import get
from json import loads
from bs4 import BeautifulSoup
from queue import SimpleQueue
import classes as c
import time

def buildLink(newStories=False, topStories=False, bestStories=False, item=None) -> str: 
    basic_URL = "https://hacker-news.firebaseio.com/v0/"
    suffix = ".json?print=pretty"

    if newStories:
        link = basic_URL+"newstories"+suffix
    elif topStories:
        link = basic_URL+"topstories"+suffix
    elif bestStories:
        link = basic_URL+"beststories"+suffix
    elif not item is None:
        link = basic_URL+'item/'+str(item)+suffix
    else:
        print('No option selected')
    
    return link


def buildStoryQueue(newStories, topStories, bestStories) -> GeneratorExit:
    hacker_news_link = buildLink(newStories, topStories, bestStories)
    top_story_ids_json = get(hacker_news_link)
    top_story_ids = loads(top_story_ids_json.content)
    story_queue = None

    for story in top_story_ids:
        
        current_story_data = loads(get(buildLink(item=story)).content)
        # implimenting because some json files do not have nessessary keys like "url", "title", or "id"
        try:
            story_queue = c.STORY(current_story_data["url"], current_story_data["title"], current_story_data["id"])
            if len(story_queue.snapshot) < 5:
                continue
        except Exception as e:
            continue
        
        yield story_queue