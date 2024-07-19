import json
import os
import uuid
from datetime import datetime

class HistoryStore:
    def __init__(self, storage_path='history_store', session_id=None):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        self.session_id = session_id or str(uuid.uuid4())
        self.date_str = datetime.now().strftime('%Y-%m-%d')
        self.history_file = os.path.join(self.storage_path, f"{self.date_str} {self.session_id}.json")
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
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)

    def load_from_disk(self):
        """Loads the history from a JSON file."""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def update_session_id(self, new_session_id):
        """Updates the session ID and reloads history from the new session file if exists."""
        self.session_id = new_session_id
        self.history_file = os.path.join(self.storage_path, f"{self.session_id}_{self.date_str}.json")
        self.history = self.load_from_disk()

    def update_entry(self, entry_id, new_data):
        pass # TODO update entry method
