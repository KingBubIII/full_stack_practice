from bs4 import BeautifulSoup
from requests import get
import DB_stuff as DB

class STORY():
    def __init__(self, link, title, hacker_news_id) -> None:
        self.hacker_news_id = hacker_news_id
        self.link = link
        self.title = title
        self.snapshot_len = 500
        self.snapshot = self.getStorySnapshot()

    def getStorySnapshot(self):
        snapshot_temp = ''
        story_web_page = get(self.link).content.decode()
        story_soup = BeautifulSoup(story_web_page, 'html.parser')
        paragraphs = story_soup.find_all('p')

        while len(snapshot_temp) < self.snapshot_len and not paragraphs == []:
            chars_left = self.snapshot_len - len(snapshot_temp)
            if len(paragraphs[0]) <= chars_left:
                snapshot_temp += paragraphs[0].text
            else:
                snapshot_temp += paragraphs[0][:chars_left]

            paragraphs.pop(0)

        return snapshot_temp + '...'

class USER():
    def __init__(self, identifier) -> None:
        self.successful, user_data = DB.login(identifier)
        self.id, self.first_name, self.email, self.password, self.join_date = user_data

    def to_json(self):        
        return {"name": self.name,
                "email": self.email}

    def is_authenticated(self):
        return self.successful

    def is_active(self):   
        return True

    def is_anonymous(self):
        return False          

    def get_id(self):
        return str(self.id)