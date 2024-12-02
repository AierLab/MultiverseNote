import json
import os
from typing import List

from app.model.dataModel import HistoryModel, MessageModel, SessionModel, RoleEnum


class HistoryManager:
    def __init__(self, history_path: str = None):
        """
        Initialize the HistoryManager with the path to the history directory.

        Args:
            history_path (str, optional): The path to the directory where session history files are stored.
                                         Defaults to None.
        """
        self.history_path = history_path or "./history"
        if not os.path.exists(self.history_path):
            os.makedirs(self.history_path)
        self.history = HistoryModel(session_id_list=[file.split(".")[0] for file in os.listdir(self.history_path)])

    def create_session(self) -> SessionModel:
        """
        Create a new session and save it to the history directory.

        Returns:
            SessionModel: The newly created session.
        """
        session = SessionModel()
        self.write_session(session)
        self.history.session_id_list.append(session.id)
        return session

    def get_session(self, session_id: str) -> SessionModel:
        """
        Load a session from the history directory by its ID.

        Args:
            session_id (str): The ID of the session to load.

        Returns:
            SessionModel: The loaded session.

        Raises:
            FileNotFoundError: If the session file does not exist.
        """
        session_file = os.path.join(self.history_path, f"{session_id}.json")
        with open(session_file, 'r') as f:
            json_data = json.load(f)
            return SessionModel(
                id=session_id,
                time_created=json_data['time_created'],
                message_list=[
                    MessageModel(
                        id=message["id"],
                        time_created=message["time_created"],
                        role=RoleEnum.get_by_name(message["role"]),
                        content=message["content"]
                    ) for message in json_data['message_list']
                ]
            )

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
        """
        Add a new message to the session and save the updated session.

        Args:
            message (MessageModel): The message to add.
            session (SessionModel): The session to which the message should be added.

        Returns:
            bool: True if the message was added successfully, False otherwise.
        """
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

        Returns:
            bool: True if the message was deleted successfully, False otherwise.
        """
        if session.delete_message(message_id):
            self.write_session(session)
            return True
        return False

    def edit_session_message(self, session: SessionModel, message_id: str, new_content: str) -> bool:
        """
        Edit the content of a message by message ID within a session and save the updated session.

        Args:
            session (SessionModel): The session containing the message to be edited.
            message_id (str): The ID of the message to be edited.
            new_content (str): The new content for the message.

        Returns:
            bool: True if the message was edited successfully, False otherwise.
        """
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