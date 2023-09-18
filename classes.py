from bs4 import BeautifulSoup
from requests import get

class STORY():
    def __init__(self, link, title, hacker_news_id) -> None:
        self.hacker_news_id = hacker_news_id
        self.link = link
        self.title = title
        self.intro_len = 500
        self.intro = self.getStoryIntro()

    def getStoryIntro(self):
        intro_temp = ''
        story_web_page = get(self.link).content.decode()
        story_soup = BeautifulSoup(story_web_page, 'html.parser')
        paragraphs = story_soup.find_all('p')

        while len(intro_temp) < self.intro_len and not paragraphs == []:
            chars_left = self.intro_len - len(intro_temp)
            if len(paragraphs[0]) <= chars_left:
                intro_temp += paragraphs[0].text
            else:
                intro_temp += paragraphs[0][:chars_left]

            paragraphs.pop(0)

        return intro_temp + '...'

