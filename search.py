import requests
from bs4 import BeautifulSoup, SoupStrainer
from googlesearch import search
import re

class Search:
    def __init__(self, title, year):
        self.title = title
        self.year = year
        self.search = self.do_search()
        self.imdb_link = self.get_imdb_link()
        if self.imdb_link != '-':
            self.omdb_id = self.imdb_link.split('/')[-2]
            self.good_match = self.check_link()
        else:
            self.good_match = False

    def do_search(self):
        query = f"{self.title} {self.year} imdb"
        print(f"Searching Google for '{self.title} ({self.year})'")
        results = search(query, lang='en', num_results=5)
        return results

    def get_imdb_link(self):
        for result in self.search:
            if 'https://www.imdb.com/title/tt' in result and result[-2].isdigit():
                return result
        else:
            return '-'

    def check_link(self):
        link = requests.get(self.imdb_link)
        only_h1 = SoupStrainer('h1')
        title_html = BeautifulSoup(link.text, 'html.parser', parse_only=only_h1)
        found_title = title_html.text

        year_html = BeautifulSoup(link.text, 'html.parser')
        nums = year_html.find_all('a')
        try:
            found_year = int([x.text for x in nums if re.match('\d{4}$', x.text[:4])][0])

            if found_year in [self.year, self.year -1, self.year -2]:
                print(f"[IMDB] Found a suitable match, correct title is: '{found_title} ({found_year})'")
                return True
            else:
                print(f"[IMDB] Couldn't find a suitable match for {self.title}")
                return False
        except AttributeError:
            print(f"[IMDB] Couldn't find a suitable match for {self.title}")
            return False



# a = Search("Rifkin'S Festiva", 2020)
# a = Search("Resident Evil: Welcome to Racoon City", 2021)
# print(a.good_match)
# a = Search("Sonic The Headgehog 2", 2022)
# a = Search("Blad", 1998)
# print(a.good_match)
# print(a.imdb_link)
# print(a.omdb_id)
# print(a.title)
# a = Search('Matrix', 1999)
# print(a.good_match)

# print(a.title)
# print(a.imdb_link)
