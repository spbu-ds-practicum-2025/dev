from rest_client import RestClient

class ConnectionManager:
    def __init__(self):
        self.rest = None
        self.ws = None

    # def connect(self, ip, port):
    #     self.rest = RestClient(f"http://{ip}:{port}")
