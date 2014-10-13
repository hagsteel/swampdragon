class BaseSessionStore(object):
    def __init__(self, connection):
        self.connection = connection
        self.keys = []

    def set(self, key, val):
        raise NotImplemented()

    def get(self, key):
        raise NotImplemented()

    def refresh_key_timeout(self, key):
        raise NotImplemented()

    def refresh_all_keys(self):
        for key in self.keys:
            self.refresh_key_timeout(key)
