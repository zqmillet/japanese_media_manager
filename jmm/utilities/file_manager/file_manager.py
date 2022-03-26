from jmm.utilities.metadata import Video
from jmm.utilities.media_finder import FileInformation

class FileManager:
    def __init__(self, destination_directory: str, mode: str):
        self.mode = mode
        self.destination_directory = destination_directory

    def manager(self, file_information: FileInformation, video: Video) -> None:
        pass
