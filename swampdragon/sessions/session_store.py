import uuid


class BaseSessionStore(object):
    def save(self, key, val):
        raise NotImplemented()

    def save_get_key(self, val):
        key = self.generate_key()
        self.save(key, val)
        return key

    def get(self, key):
        raise NotImplemented()

    def generate_key(self):
        key = uuid.uuid4()
        return key.hex

    def refresh_key_timeout(self, key):
        raise NotImplemented()
