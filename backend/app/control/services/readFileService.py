# Read local file

class ReadFileService:
    def read_text_file(self, file_path: str) -> str:
        """
        Reads and returns the content of a text file.

        Args:
            file_path (str): The path to the text file.

        Returns:
            str: The content of the text file.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there is an error reading the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file at path {file_path} was not found.") from e
        except IOError as e:
            raise IOError(f"An error occurred while reading the file at path {file_path}.") from e

    def read_json_file(self, file_path: str) -> dict:
        """
        Reads a JSON formatted file and returns its content.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The content of the JSON file as a dictionary.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there is an error reading the file.
            json.JSONDecodeError: If there is an error decoding the JSON file.
        """
        import json
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file at path {file_path} was not found.") from e
        except IOError as e:
            raise IOError(f"An error occurred while reading the file at path {file_path}.") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"An error occurred while decoding the JSON file at path {file_path}.", e.doc, e.pos) from e