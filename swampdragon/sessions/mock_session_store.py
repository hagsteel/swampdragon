from .session_store import BaseSessionStore

sessions = {}


class MockSessionStore(BaseSessionStore):
    def save(self, key, val):
        sessions[key] = val

    def get(self, key):
        try:
            return sessions[key]
        except:
            return None
