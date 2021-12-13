from radarr import Radarr
from tmdb import TMDB
from omdb import OMDB
from datetime import datetime

YEAR = datetime.now().year

class Movie:
    def __init__(self, title, date, genres, running_time, image, link, presale=False):
        self.title = title
        self.date = date
        self.genres = genres
        self.running_time = running_time
        self.presale = presale
        self.image = image
        self.link = link
        self.omdb = OMDB(self.title, YEAR)
        if self.omdb.is_in_omdb:
            self.title = self.omdb.title
        self.tmdb = TMDB(self.title, YEAR)
        self.radarr = Radarr(self.tmdb.tmdb_id)
        self.is_wanted = self.radarr.found
        self._genres()

    def _genres(self):
        if self.omdb.genres != '-':
            self.genres = self.omdb.genres

    def __str__(self):
        string = f"""
        Title: {self.title}
        Date: {self.date}
        Genres: {", ".join(self.genres)}
        Country: {self.omdb.country}
        Language: {self.omdb.language}
        Runtime: {self.running_time}
        Director: {self.omdb.director}
        Actors: {self.omdb.actors}
        Is Wanted?: {self.is_wanted}
        Presale: {self.presale}
        Poster: {self.image}
        Link: {self.link}
        """
        return string
