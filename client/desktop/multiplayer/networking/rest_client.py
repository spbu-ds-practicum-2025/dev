import requests

class RestClient:
    def __init__(self, base_url):
        self.base = base_url

    # def get_rooms(self):
    #     return requests.get(f"{self.base}/rooms").json()
