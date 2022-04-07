import requests
from bs4 import BeautifulSoup, SoupStrainer
from googlesearch import search
from datetime import datetime
import re

YEAR = datetime.now().year

class Search:
    def __init__(self, title):
        self.title = title
        self.main()

    def main(self):
        self.search = self.do_search()
        self.imdb_link = self.get_imdb_link()
        if self.imdb_link != '-':
            self.omdb_id = self.imdb_link.split('/')[-2]
            self.good_match = self.check_link()
        else:
            self.good_match = False

    def do_search(self):
        query = self.title + f' imdb'
        print(f"[GOOGLE] Searching for '{self.title}'..")
        results = search(query, lang='en', num_results=10)
        return results

    def get_imdb_link(self):
        for result in self.search:
            if 'imdb.com/title' in result:
                print("[GOOGLE] Found a possible match..")
                return result
        else:
            print("[GOOGLE] Couldn't find a match..")
            return '-'

    # def check_link(self):
    #     link = requests.get(self.imdb_link)
    #     html = BeautifulSoup(link.text, 'html.parser')
    #     table = html.find('div', ('class', ('TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt')))  # !Probable point of failure
    #     found_year = int(table.find('a').text)
    #     found_title = table.find('h1').text
    #     if found_year == YEAR or found_year == YEAR -1 or found_year == YEAR -2:
    #         print(f"[IMDB] Found a suitable match, correct title is: '{found_title} ({found_year})'")
    #         return True
    #     else:
    #         print(f"[IMDB] Couldn't find a suitable match for {self.title}")
    #         return False

    def check_link(self):
        link = requests.get(self.imdb_link)
        only_h1 = SoupStrainer('h1')
        title_html = BeautifulSoup(link.text, 'html.parser', parse_only=only_h1)
        found_title = title_html.text

        year_html = BeautifulSoup(link.text, 'html.parser')
        nums = year_html.find_all('a')
        found_year = int([x.text for x in nums if re.match('\d{4}$', x.text[:4])][0])

        if found_year == YEAR or found_year == YEAR -1 or found_year == YEAR -2:
            print(f"[IMDB] Found a suitable match, correct title is: '{found_title} ({found_year})'")
            return True
        else:
            print(f"[IMDB] Couldn't find a suitable match for {self.title}") # self
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
# a = Search("El Paseo 6")
