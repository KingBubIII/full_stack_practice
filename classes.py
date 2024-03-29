from bs4 import BeautifulSoup
from requests import get
import DB_stuff as DB

class STORY():
    def __init__(self, error:bool, hacker_news_id:int, link:str=None, title:str=None, date_saved=None) -> None:
        self._error = error
        self.hacker_news_id = hacker_news_id
        self._snapshot_len = 500

        if not error:
            self.link = link
            self.title = title
            self.date_saved = date_saved
            self.snapshot = self.getStorySnapshot()
        else:
            self.link = "Error"
            self.title = "Error"
            self.date_saved = date_saved
            self.snapshot = "Could not find story snapshot"

    def getStorySnapshot(self):
        snapshot_temp = ''
        story_web_page = get(self.link).content.decode()
        story_soup = BeautifulSoup(story_web_page, 'html.parser')
        paragraphs = story_soup.find_all('p')

        while len(snapshot_temp) < self._snapshot_len and not paragraphs == []:
            chars_left = self._snapshot_len - len(snapshot_temp)
            if len(paragraphs[0].text) <= chars_left:
                snapshot_temp += paragraphs[0].text
            else:
                snapshot_temp += str(paragraphs[0])[:chars_left]

            paragraphs.pop(0)

        return snapshot_temp + '...'

class USER():
    def __init__(self, identifier) -> None:
        self.successful, user_data = DB.login(identifier)
        if not self.successful:
            return
        self.id, self.first_name, self._email, self._password, self._join_date = user_data

        self.is_anonymous = False
        self.is_active = True
        self.is_authenticated = self.successful


    def to_json(self):
        return {"name": self.name,
                "email": self.email}

    def get_id(self):
        return str(self.id)