# Read local file

class ReadFileService:
    def read_text_file(self, file_path):
        """Reads and returns the content of a text file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def read_json_file(self, file_path):
        """Reads a JSON formatted file and returns its content."""
        import json
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
