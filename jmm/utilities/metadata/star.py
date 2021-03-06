from PIL.JpegImagePlugin import Image

from jmm.utilities.functions import image_to_ascii

class Star:
    def __init__(self, avatar_url: str, avatar: Image, name: str):
        self.avatar = avatar
        self.avatar_url = avatar_url
        self.name = name

    def __repr__(self) -> str:
        return f"<star {self.name}, {self.avatar_url}>\n{image_to_ascii(self.avatar, columns=20)}"
