import json
import os
from typing import List

from app.model.dataModel import HistoryModel
from app.model.dataModel import MessageModel, SessionModel, RoleEnum


class HistoryManager:
    def __init__(self, history_path: str = None):
        self.history_path = history_path
        if not os.path.exists(self.history_path):
            os.makedirs(self.history_path)
        self.history = HistoryModel(session_id_list=[file.split(".")[0] for file in os.listdir(self.history_path)])

    def create_session(self):
        session = SessionModel()
        self.write_session(session)
        self.history.session_id_list.append(session.id)
        return session

    def get_session(self, session_id: str) -> SessionModel:
        session_file = os.path.join(self.history_path, f"{session_id}.json")
        with open(session_file, 'r') as f:
            json_data = json.load(f)
            return SessionModel(id=session_id,
                                time_created=json_data['time_created'],
                                message_list=[MessageModel(id=message["id"], time_created=message["time_created"],
                                                                 role=RoleEnum.get_by_name(message["role"]),
                                                                 content=message["content"]) for message in
                                                    json_data['message_list']],
                                vector_store_id=json_data['vector_store_id'])

    def write_session(self, session: SessionModel):
        """
        Write the session data to a JSON file.

        Args:
            session (SessionModel): The session model to be serialized and saved.
        """
        session_file = os.path.join(self.history_path, f"{session.id}.json")
        json_data = session.serialize()

        with open(session_file, 'w') as f:
            json.dump(json_data, f, indent=4)

    def add_session_message(self, message: MessageModel, session: SessionModel) -> bool:
        """Add a new entry to the history."""
        if session.add_message(message):
            self.write_session(session)
            return True
        return False

    def delete_session_message(self, session: SessionModel, message_id: str) -> bool:
        """
        Delete a message from the session by message ID and save the updated session.

        Args:
            session (SessionModel): The session from which to delete the message.
            message_id (str): The ID of the message to be deleted.
        """
        if session.delete_message(message_id):
            self.write_session(session)
            return True
        return False

    def edit_session_message(self, session: SessionModel, message_id: str, new_content: str) -> bool:
        """Edit the content of a message by message ID within a session and save the updated session."""
        if session.edit_message_content(message_id, new_content):
            self.write_session(session)
            return True
        return False

    def get_all_sessions(self) -> List[SessionModel]:
        """
        Retrieve all session files from the history path and return them as a list of SessionModel instances.

        Returns:
            list[SessionModel]: A list containing all the loaded session models.
        """
        sessions = []
        # List all files in the directory
        for filename in os.listdir(self.history_path):
            # Check if the file is a JSON file
            if filename.endswith('.json'):
                # Extract the session ID from the filename
                session_id = filename[:-5]  # Remove the '.json' part
                # Load the session using the existing load_session method
                session = self.get_session(session_id)
                sessions.append(session)
        return sessions

    def delete_session(self, session_id: str) -> bool:
        """
        Delete the session file associated with the given session_id.

        Args:
            session_id (str): The ID of the session to delete.

        Returns:
            bool: True if the file was successfully deleted, False otherwise.
        """
        # Construct the path to the session file
        session_file = os.path.join(self.history_path, f"{session_id}.json")

        # Check if the file exists
        if os.path.exists(session_file):
            # Delete the file
            os.remove(session_file)
            self.history.session_id_list.remove(session_id)
            return True
        else:
            # Return False if the file does not exist
            print(f"Warning: The session file for session_id '{session_id}' does not exist.")
            return False
