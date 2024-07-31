import os
import shutil
import unittest

from app.dao.historyDataManager import HistoryManager
from app.model.dataModel import MessageModel, RoleEnum


class TestHistoryStore(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.storage_path = 'test_history_store'
        self.history_store = HistoryManager(history_path=self.storage_path)
        self.session = self.history_store.create_session()

    def test_add_and_get_message(self):
        """Test adding an entry and retrieving it."""
        test_message = MessageModel(content="hi", role=RoleEnum.USER)
        self.history_store.add_session_message(test_message, self.session)
        session_loaded = self.history_store.get_session(session_id=self.session.id)
        self.assertIn(test_message, session_loaded.message_list)

    def test_delete_entry(self):
        """Test deleting an entry."""
        test_message = MessageModel(content="hi", role=RoleEnum.USER)
        self.history_store.add_session_message(test_message, self.session)
        test_session = self.history_store.get_session(session_id=self.session.id)
        self.history_store.delete_session_message(test_session, test_message.id)
        self.assertNotIn(test_message, test_session.message_list)

    def tearDown(self):
        """Clean up after tests are done."""
        if os.path.exists(self.storage_path):
            shutil.rmtree(self.storage_path)


if __name__ == '__main__':
    unittest.main()
