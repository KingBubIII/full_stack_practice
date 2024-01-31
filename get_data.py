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

def getStoryItem(story_id, date_saved=None):
    story_data = loads(get(buildLink(story_id)).content)
    try:
        story_class = c.STORY(error=False, link=story_data["url"], title=story_data["title"], hacker_news_id=story_data["id"], date_saved=date_saved)
    except Exception as e:
        print(e)
        story_class = c.STORY(error=True, hacker_news_id=story_id)
    return story_class

def buildStoryQueue(story_type) -> GeneratorExit:
    hacker_news_link = buildLink(story_type)
    top_story_ids_json = get(hacker_news_link)
    story_ids = loads(top_story_ids_json.content)
    story_class = None

    for story_id in story_ids:
        # implimenting because some json files do not have nessessary keys like "url", "title", or "id"
        story_class = getStoryItem(story_id)
        if len(story_class.snapshot) < 5 or story_class._error:
            continue
        
        yield story_class