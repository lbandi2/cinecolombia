import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
from movie import Movie
from db import add_records, delete_records
from utils import replace_str

class Page:
    DIR_PATH = f"{os.path.dirname(os.path.realpath(__file__))}"
    def __init__(self, url, filename):
        self.url = url
        self.filename = f'./webpages/{filename}'
        self.soup = ''
        self.movies = []
        self.main()

    def main(self):
        self.startup_check()
        page = self.grab_page(self.url)
        self.save_page(page, self.filename)
        self.soup = self.load_page(self.filename)
        if 'playing' in self.filename:
            delete_records('playing')
        elif 'upcoming' in self.filename:
            delete_records('upcoming')
        self.parse_page()
        print(f"Found {len(self.movies)} movies.")
        for index, movie in enumerate(self.movies, start=1):
            print(index, movie.title)

    def startup_check(self):
        if os.path.isdir(f"{self.DIR_PATH}/webpages") == False:
            self.make_dir('webpages')
        if os.path.isdir(f"{self.DIR_PATH}/logs") == False:
            self.make_dir('logs')

    def make_dir(self, dir_name):
        try:
            path = os.path.join(self.DIR_PATH, dir_name)
            os.mkdir(path)
        except OSError:
            print (f"Creation of the directory '{dir_name}' failed")
        else:
            print(f"Successfully created folder '{dir_name}'..")		

    def grab_page(self, url):
        webpage = requests.get(url)
        content = webpage.content
        print("Grabbing webpage..")
        return content
    
    def save_page(self, content, filename):
        with open(filename, 'wb') as webpage:
            webpage.write(content)

    def load_page(self, filename):
        with open(filename, 'r', encoding="utf-8") as webpage:
            return BeautifulSoup(webpage, 'html.parser')

    def find_title_spanish(self, soup):
        title = soup.find('h2', ('class', ('movie-item__title')))
        return title.text

    def find_title_english(self, soup):
        try:
            table = soup.find('div', ('class', ('movie-item__basics')))
            title = table.find('span', ('class', ('movie-item__meta--bold')))
            title = re.split('T.tulo en ingl.s:', title.text)[-1].strip()
            return title
        except:
            return '-'

    def find_date(self, soup):
        rep = {
            "ene": "jan",
            "abr": "apr",
            "ago": "aug",
            "sept": "sep",
            "dic": "dec"
            }

        table = soup.find_all('span', ('class', ('movie-item__meta')))
        for x in table:
            if 'Estreno:' in x.text:
                estreno = replace_str(x.text.split('Estreno:')[-1].strip().lower(), rep)
                try:
                    date = datetime.strptime(estreno, "%d-%b-%Y").strftime("%Y-%m-%d")
                    return date
                except ValueError:
                    print("[ERROR] Could not process date")
                    return None

    def find_genres(self, soup):
        clean_genres = []
        table = soup.find_all('span', ('class', ('movie-item__meta')))
        for x in table:
            if re.search('G.nero:', x.text):
                genres = re.split('G.nero:', x.text)[-1].split(',')
                for x in genres:
                    clean_genres.append(x.strip())
                return clean_genres

    def find_running_time(self, soup):
        table = soup.find('div', ('class', ('movie-item__tags')))
        for x in table:
            try:
                if 'Min' in x.text:
                    return x.text.split(' Min')[0]
            except AttributeError:
                pass
        else:
            return None

    def find_link(self, soup):
        table = soup.find('a', ('class', ('movie-item')))
        link = table.get('href')
        cineurl = 'https://www.cinecolombia.com'
        return cineurl + link

    def find_image(self, soup):
        table = soup.find('a', ('class', ('movie-item'))).find('div', ('class', ('movie-item__image-wrapper')))
        image = table.find('img').get('data-src')
        return image

    def find_presale(self, soup):
        try:
            table = soup.find('a', ('class', ('movie-item'))).find('div', ('class', ('movie-item__image-wrapper')))
            presale = table.find('span', ('class', ('movie-item__badge'))).text
            if 'Preventa' in presale:
                return True
            return False
        except AttributeError:
            return False

    def parse_page(self):
        table = self.soup.find_all('div', ('class', ('column is-3')))
        for x in table:
            title_spanish = self.find_title_spanish(x)
            title_english = self.find_title_english(x)
            if title_english != '-':
                title = title_english
            else:
                title = title_spanish

            date = self.find_date(x)
            genres = self.find_genres(x)
            running_time = self.find_running_time(x)
            link = self.find_link(x)
            image = self.find_image(x)
            presale = self.find_presale(x)

            movie = Movie(title, date, genres, running_time, image, link, presale)
            self.movies.append(movie)
            if 'playing' in self.filename:
                add_records(movie, 'playing')
            elif 'upcoming' in self.filename:
                add_records(movie, 'upcoming')

