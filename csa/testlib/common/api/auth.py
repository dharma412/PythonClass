from requests.auth import HTTPBasicAuth

class BasicAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_auth(self):
        return HTTPBasicAuth(self.username, self.password)

class JwtAuth:
    pass