class User:
    def __init__(self, username, password, recovery=None):
        self.username = username
        self.__password = password
        self.recovery = recovery

    @property
    def password(self):
        return self.__password
