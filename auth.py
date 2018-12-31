from config import *
from files import Files

class Auth(Files):

    def check_auth(self, auth):
        return len(self.get_auth()) > 0 and str(auth) == self.get_auth()

    def get_auth(self):
        return self.file_read(AUTH_FILE)

    def save_auth(self, auth):
        return self.file_write(AUTH_FILE, auth)