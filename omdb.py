import requests
from secrets import json_secret
from search import Search

URL = 'http://www.omdbapi.com/'
OMDB_API = json_secret('omdb', 'api_key')

class OMDB:
    def __init__(self, title, year):
        self.url = 'http://www.omdbapi.com/'
        self.title = title
        self.year = year

        if not self.is_in_omdb():
            self.search = Search(self.title, self.year)
            if self.search.good_match:
                if self.search_by_id(self.search.omdb_id):
                    self.is_in_omdb()

    def search_by_id(self, id):
        query_omdb = \
            {
                'apikey': OMDB_API,
                'i': id
            }
        resp = requests.get(URL, params=query_omdb)
        json_response = resp.json()

        if resp.status_code == 200:
            if json_response['Response'] == 'True':
                title = json_response['Title']
                year = json_response['Year']
                # print(f"[OMDB] Found searched movie '{title} ({year})'.")
                self.get_fields(json_response)
                return True
        else:
            return False

    def get_fields(self, json):
        self.title = json['Title']
        self.year = json['Year']

    def is_in_omdb(self):
        """Return attributes if movie is found in IMDB."""

        year = int(self.year)
        years = [year, year - 1, year - 2]
        title = self.title.replace("&", "")

        for x in years:
            query_omdb = \
                {
                    'apikey': OMDB_API,
                    't': title,
                    'y': x
                }

            resp = requests.get(self.url, params=query_omdb)

            # http://www.omdbapi.com/?apikey=5705b52c&t=why%20me&y=2020

            json_response = resp.json()

            if resp.status_code == 200:
                if json_response['Response'] == 'True':
                    print(f"[OMDB] Found movie '{self.title}'.")
                    self.get_attributes(json_response)
                    return True
        else:
            print(f"[OMDB] Couldn't find movie '{self.title}'.")
            self.get_attributes(json_response)
            return False

    def get_attributes(self, response):
        try:
            self.imdb_id = f"https://www.imdb.com/title/{response['imdbID']}"
            self.country = response['Country'].split(",")[0]
            self.genres = response['Genre'].lower().split(", ")
            self.runtime = response['Runtime'].split(" ")[0]
            self.year = int(response['Year'])
            self.director = response['Director']
            self.actors = response['Actors']
            self.language = response['Language']
            self.poster = response['Poster']
        except KeyError:
            self.imdb_id = '-'
            self.language = '-'
            self.actors = '-'
            self.director = '-'
            self.runtime = '-'
            self.genres = '-'
            self.country = '-'
            self.poster = '-'

    def __str__(self):
        string = f"""
        ID: {self.imdb_id}
        Title: {self.title}
        Year: {self.year}
        Country: {self.country}
        Language: {self.language}
        Genres: {self.genres}
        Runtime: {self.runtime}
        Director: {self.director}
        Actors: {self.actors}
        Poster: {self.poster}
        """
        return string


# a = OMDB('TeSigo', 2021)
# a = OMDB('Encanto', 2021)
# a = OMDB('Resident Evil Welcome to Racoon City', 2021)
# a = OMDB('El Paseo 6', '-')
# print(a)
# a = search_by_id('tt8593904')
# print(a)