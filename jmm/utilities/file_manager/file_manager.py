from jmm.utilities.metadata import Video
from jmm.utilities.media_finder import FileInformation

class FileManager:
    def __init__(self, mode: str = 'infuse'):
        self.mode = mode

    def manager(self, file_information: FileInformation, video: Video) -> None:
        pass
