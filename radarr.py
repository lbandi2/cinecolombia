import requests
from secrets import get_secret

RADARR_URL = get_secret('radarr_url')
RADARR_API = get_secret('radarr_api')

class Radarr:
    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id
        self.url = RADARR_URL
        self.found = self.is_in_radarr()

    def is_radarr_running(self):
        try:
            req = requests.get(self.url)
            if req.status_code == 200:
                return True
        except:
            return False

    def is_in_radarr(self):
        """Checks if a movie is already in Radarr."""
        if self.is_radarr_running():
            radarr_endpoint = f'{self.url}api/v3/movie?'
            query_radarr = \
                {
                    'apikey': RADARR_API,
                    'tmdbId': self.tmdb_id
                }

            resp = requests.get(radarr_endpoint, params=query_radarr)
            json_response = resp.json()

            if resp.status_code == 200:
                if json_response != []:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

