from requests import get
from json import loads
import classes as c

def buildLink(item:str) -> str: 
    basic_URL = "https://hacker-news.firebaseio.com/v0/"
    suffix = ".json?print=pretty"

    if type(item) is int:
        link = basic_URL+'item/'+str(item)+suffix
    else:
        link = basic_URL+item+suffix
    
    return link

def getStoryItem(story_id):
    story_data = loads(get(buildLink(story_id)).content)
    story_class = c.STORY(story_data["url"], story_data["title"], story_data["id"])
    return story_class

def buildStoryQueue(story_type) -> GeneratorExit:
    hacker_news_link = buildLink(story_type)
    top_story_ids_json = get(hacker_news_link)
    top_story_ids = loads(top_story_ids_json.content)
    story_class = None

    for story in top_story_ids:
        # implimenting because some json files do not have nessessary keys like "url", "title", or "id"
        try:
            story_class = getStoryItem(story)
            if len(story_class.snapshot) < 5:
                continue
        except Exception as e:
            continue
        
        yield story_class