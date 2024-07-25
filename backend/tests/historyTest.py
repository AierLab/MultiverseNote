import os
import shutil
import unittest

from app.control.database import HistoryStore


class TestHistoryStore(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.storage_path = 'test_history_store'
        self.history_store = HistoryStore(storage_path=self.storage_path)

    def test_add_and_retrieve_entry(self):
        """Test adding an entry and retrieving it."""
        test_entry = {'id': 1, 'text': 'Test entry'}
        self.history_store.add_entry(test_entry)
        entries = self.history_store.retrieve_all()
        self.assertIn(test_entry, entries)

    def test_delete_entry(self):
        """Test deleting an entry."""
        test_entry = {'id': 1, 'text': 'Test entry'}
        self.history_store.add_entry(test_entry)
        self.history_store.delete_entry(1)
        entries = self.history_store.retrieve_all()
        self.assertNotIn(test_entry, entries)

    def tearDown(self):
        """Clean up after tests are done."""
        if os.path.exists(self.storage_path):
            shutil.rmtree(self.storage_path)


if __name__ == '__main__':
    unittest.main()
