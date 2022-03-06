from shutil import get_terminal_size
from typing import Optional
from PIL.JpegImagePlugin import JpegImageFile
from ascii_magic import from_image

def image_to_ascii(image: JpegImageFile, columns: Optional[int] = None) -> str:
    columns = columns or get_terminal_size().columns
    return from_image(image, columns)
