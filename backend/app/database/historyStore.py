# Manages the storage and retrieval of conversation history data in the database.

import json
import os

class HistoryStore:
    def __init__(self, storage_path='history_store'):
        self.storage_path = storage_path
        self.history_file = os.path.join(storage_path, 'history.json')
        self.history = self.load_from_disk()

    def add_entry(self, entry):
        """Add a new entry to the history."""
        self.history.append(entry)
        self.save_to_disk()

    def retrieve_all(self):
        """Retrieve all history entries."""
        return self.history

    def delete_entry(self, entry_id):
        """Delete an entry from the history by ID."""
        self.history = [entry for entry in self.history if entry['id'] != entry_id]
        self.save_to_disk()

    def save_to_disk(self):
        """Saves the history to a JSON file."""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)

    def load_from_disk(self):
        """Loads the history from a JSON file."""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []