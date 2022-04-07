import requests
from bs4 import BeautifulSoup
import re
from movie import Movie

class Page:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.type = self.filename.split('.')[0].split('_')[1]
        self.soup = ''
        self.movies = []
        self.main()

    def main(self):
        page = self.grab_page(self.url)
        self.save_page(page, self.filename)
        self.soup = self.load_page(self.filename)
        self.parse_page()

        print(f"\nFound {len(self.movies)} {self.type} movies:")
        for x in self.movies:
            print(f"- {x.title}")
        
    def grab_page(self, url):
        webpage = requests.get(url)
        content = webpage.content
        print(f"\nGrabbing webpage..")
        return content
    
    def save_page(self, content, filename):
        with open(f'./{filename}', 'wb') as webpage:
            webpage.write(content)

    def load_page(self, filename):
        with open(f'./{filename}', 'r', encoding="utf-8") as webpage:
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
        table = soup.find_all('span', ('class', ('movie-item__meta')))
        for x in table:
            if 'Estreno:' in x.text:
                estreno = x.text.split('Estreno:')[-1].strip()
                return estreno

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
            return '-'

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

            self.movies.append(Movie(title, date, genres, running_time, image, link, presale))
