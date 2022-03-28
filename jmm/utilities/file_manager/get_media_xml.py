from typing import Optional
from bs4 import BeautifulSoup
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from jmm.utilities.media_finder import FileInformation
from jmm.utilities.metadata import Video
from jmm.utilities.translator import Translator

def get_media_xml(file_information: FileInformation, video: Video, translator: Optional[Translator] = None):
    movie = Element('movie')
    SubElement(movie, 'title').text = video.title
    SubElement(movie, '').text = video.title
    soup = BeautifulSoup(tostring(movie, encoding='utf8'))
    print(soup.prettify())
    import pdb; pdb.set_trace()
