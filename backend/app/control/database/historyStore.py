import json
import os
import uuid
from datetime import datetime


class HistoryStore:
    def __init__(self, history_path=None, session_id=None):
        self.history_path = history_path
        if not os.path.exists(self.history_path):
            os.makedirs(self.history_path)
        self.session_id = session_id or str(uuid.uuid4())
        self.date_str = datetime.now().strftime('%Y-%m-%d')
        self.session_file = os.path.join(self.history_path, f"{self.date_str} {self.session_id}.json")
        self.session = self.load_from_disk()

    def add_entry(self, entry):
        """Add a new entry to the history."""
        self.session.append(entry)
        self.save_to_disk()

    def retrieve_all(self):
        """Retrieve all history entries."""
        return self.session

    def delete_entry(self, entry_id):
        """Delete an entry from the history by ID."""
        self.session = [entry for entry in self.session if entry['id'] != entry_id]
        self.save_to_disk()

    def save_to_disk(self):
        """Saves the history to a JSON file."""
        with open(self.session_file, 'w') as f:
            json.dump(self.session, f)

    def load_from_disk(self):
        """Loads the history from a JSON file."""
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return []

    def update_session_id(self, new_session_id):
        """Updates the session ID and reloads history from the new session file if exists."""
        self.session_id = new_session_id
        self.session_file = os.path.join(self.history_path, f"{self.session_id}_{self.date_str}.json")
        self.session = self.load_from_disk()

    def update_entry(self, entry_id, new_data):
        pass  # TODO update entry method
