class FilePath:
    def __init__(self, file_directory: str, filename: str):
        self.file_directory = file_directory
        self.filename = filename

    def get_file_path(self) -> str:
        return f"{self.file_directory}/{self.filename}"

    def get_file_directory(self) -> str:
        return self.file_directory

    def get_filename(self) -> str:
        return self.filename
