import requests
from secrets import get_secret
from utils import replace_str

TMDB_API = get_secret('tmdb_api')

class TMDB:
    def __init__(self, movie, year):
        self.title = movie
        self.year = year
        self.main()

    def main(self):
        self.is_in_tmdb()
        self.title_slug = self.get_slug()

    def is_in_tmdb(self):
        """Return attributes if movie is found in TMDB."""

        dif_list = [0, -1, -2]
        tmdb_url = 'https://api.themoviedb.org/3/search/movie?'

        # check if current year, next year or previous year match in tmdb
        if type(self.year) == int:
            for dif in dif_list:

                query_tmdb = \
                    {
                        'api_key': TMDB_API,
                        'language': 'en-US',
                        'query': self.title,
                        'page': 1,
                        'include_adult': 'false',
                        'year': int(self.year) + dif
                    }
                resp = requests.get(tmdb_url, params=query_tmdb)
                json_response = resp.json()

                if resp.status_code == 200 and json_response['total_results'] != 0:
                    print(f"[TMDB] Found movie '{self.title}'.")
                    self.get_attributes(json_response)
                    return True
            else:
                print(f"[TMDB] Couldn't find movie '{self.title}'.")
                self.get_attributes(json_response)
                return False
        else:
            return False

    def get_attributes(self, response):
        try:
            self.tmdb_id = response['results'][0]['id']
            self.title = response['results'][0]['title']
            self.year = int(response['results'][0]['release_date'].split('-')[0])
            self.plot = response['results'][0]['overview']
            if response['results'][0]['vote_average'] != 0:
                self.rating = response['results'][0]['vote_average']
            else:
                self.rating = '-'
            self.poster = f"https://image.tmdb.org/t/p/w500{response['results'][0]['poster_path']}"
            self.poster_small = f"https://image.tmdb.org/t/p/w154{response['results'][0]['poster_path']}"
        except IndexError:
            self.title = '-'
            # self.year = '-'
            self.tmdb_id = '-'
            self.plot = '-'
            self.rating = '-'
            self.poster = '-'
            self.poster_small = '-'

    def get_slug(self):
        """Return slug for current movie title."""

        rep = {"&": "and",
               "$": "",
               " - ": "-",
               " ": "-",
               ":": "",
               "'": "",
               ".": ""}

        if self.tmdb_id != '-':
            slug = replace_str(self.title.lower(), rep)
            return f"{slug}-{str(self.tmdb_id)}"

    def __str__(self):
        string = f"""
        ID: {self.tmdb_id}
        Title: {self.title}
        Plot: {self.plot}
        Rating: {self.rating}
        Poster: {self.poster}
        Poster_small: {self.poster_small}
        """
        return string

# a = TMDB('#TeSigo', 2021)
# a = TMDB('Resident Evil: Welcome to Racoon City', 2021)
# a = TMDB('Matrix Revolutions', 2003)
# print(a.plot)
