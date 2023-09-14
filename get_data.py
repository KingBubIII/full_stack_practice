from requests import get
import json

basic_URL = "https://hacker-news.firebaseio.com/v0/"
suffix = ".json?print=pretty"
top_story_ids_json = get(basic_URL+"topstories"+suffix)
top_story_ids = json.loads(top_story_ids_json.content)