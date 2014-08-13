from .dragon_test_case import DragonTestCase
from ..sessions.mock_session_store import MockSessionStore


class SessionTest(DragonTestCase):
    def setUp(self):
        self.session_store = MockSessionStore()

    def test_save_sessions(self):
        key = 'foo'
        val = 'bar'

        self.session_store.save(key, val)
        actual = self.session_store.get(key)
        self.assertEqual(val, actual)

    def test_save_sessions_get_key(self):
        val = 'bar'
        key = self.session_store.save_get_key(val)
        actual = self.session_store.get(key)
        self.assertEqual(val, actual)
