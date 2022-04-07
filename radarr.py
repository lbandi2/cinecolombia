import requests
from secrets import get_secret

RADARR_URL = get_secret('radarr_url')
RADARR_API = get_secret('radarr_api')

class Radarr:
    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id
        self.url = RADARR_URL
        self.api_key = RADARR_API
        self.endpoint = f'{self.url}api/v3/movie?apikey={self.api_key}'
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

            query_radarr = \
                {
                    'tmdbId': self.tmdb_id
                }

            resp = requests.get(self.endpoint, params=query_radarr)
            json_response = resp.json()

            if resp.status_code == 200:
                if json_response != []:
                    return True

        return False

    def get_jsondata(self):
        if self.is_radarr_running():
            if self.is_in_radarr():

                query_radarr = \
                    {
                        'tmdbId': self.tmdb_id
                    }
                
                resp = requests.get(self.endpoint, params=query_radarr)
                json_response = resp.json()

                return json_response

    def get_tags(self):
        if self.is_radarr_running():
            if self.is_in_radarr():
                json_query = self.get_jsondata()

                return json_query[0]['tags']

    def check_tag(self, tag):
        json_query = self.get_jsondata()
        if tag in json_query[0]['tags']:
            return True
        else:
            return False

    def add_tag(self, tag):
        if not self.check_tag(tag):
            json_query = self.get_jsondata()
            json_query[0]['tags'].append(tag)

            resp = requests.put(self.endpoint, json=json_query[0])
            json_response = resp.json()

            if 'message' in json_response:
                print(json_response['message'])
            else:
                print("Added tag")
        else:
            print("Tag exists")

    def remove_tag(self, tag):
        if self.check_tag(tag):
            json_query = self.get_jsondata()
            json_query[0]['tags'].remove(tag)

            resp = requests.put(self.endpoint, json=json_query[0])
            json_response = resp.json()

            if 'message' in json_response:
                print(json_response['message'])
            else:
                print("Removed tag")
                self.get_tags()
        else:
            print("Tag not found") 
                    
                    # ? Esto
                    # ! Eso
                    # * Raro
                    # // Pepe
                    # TODO: lalala
                    # FIXME: papapap
                    # TODO: pepepe



# a = Radarr(460458) 
# a = Radarr(614917)
# print(a.tags)
# a.add_tag(3)
# a.remove_tag(3)
# print(a.tags)
# a = Radarr(271110)
# a = Radarr(68721)
# print(a.is_in_radarr())

# 7.1 // TrueHD Atmos
# 5.1 // EAC3 Atmos
# 5.1 // DTS-HD MA
# 5.1 // AC3
# 2   // EAC3
# 5.1 // DTS
