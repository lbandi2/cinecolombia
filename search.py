import requests
from bs4 import BeautifulSoup
from googlesearch import search
from datetime import datetime

YEAR = datetime.now().year

class Search:
    def __init__(self, title):
        self.title = title
        self.search = self.do_search()
        self.imdb_link = self.get_imdb_link()
        if self.imdb_link != '-':
            self.omdb_id = self.imdb_link.split('/')[-2]
            self.good_match = self.check_link()
        else:
            self.good_match = False

    def do_search(self):
        query = self.title + ' 2021 imdb'
        print(f"Searching Google for '{self.title}'")
        results = search(query, lang='en', num_results=5)
        return results

    def get_imdb_link(self):
        for x in self.search:
            if 'imdb.com/title' in x:
                return x
        else:
            return '-'

    def check_link(self):
        link = requests.get(self.imdb_link)
        html = BeautifulSoup(link.text, 'html.parser')
        table = html.find('div', ('class', ('TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt')))  ### this could fail
        found_year = int(table.find('a').text)
        if found_year == YEAR or found_year == YEAR -1:
            return True
        else:
            return False



# a = Search("Rifkin'S Festiva")
# a = Search("Resident Evil: Welcome to Racoon City")
# print(a.good_match)
# a = Search("#TeSigo")
# print(a.good_match)
# print(a.imdb_link)
# print(a.omdb_id)
# print(a.title)
# a = Search('El Paseo 6')
# print(a.good_match)

# print(a.title)
# print(a.imdb_link)
