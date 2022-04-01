from os.path import join
from os import makedirs
from shutil import move
from typing import Optional
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom

from jmm.utilities.metadata import Video
from jmm.utilities.media_finder import FileInformation
from jmm.utilities.translator import Translator
from jmm.utilities.translator import TranslationException

class FileManager:
    def __init__(self, destination_directory: str, mode: str, translator: Optional[Translator] = None):
        self.mode = mode
        self.destination_directory = destination_directory
        self.translator = translator

    def manager(self, file_information: FileInformation, video: Video) -> str:
        directory = join(self.destination_directory, video.number)
        media_file_name = f'{video.number}{file_information.file_path.suffix}'
        nfo_file_name = f'{video.number}.nfo'
        fanart_file_name = f'{video.number}-fanart.jpg'
        poster_file_name = f'{video.number}-poster.jpg'

        makedirs(directory, exist_ok=True)
        move(file_information.file_path, join(directory, media_file_name))

        with open(join(directory, nfo_file_name), 'w', encoding='utf8') as file:
            file.write(self.get_xml_string(file_information, video))

        if video.fanart:
            video.fanart.save(join(directory, fanart_file_name))

        if video.poster:
            video.poster.save(join(directory, poster_file_name))

        return directory

    def translate(self, text: Optional[str]) -> str:
        if text is None:
            return ''

        if not self.translator:
            return text

        try:
            return self.translator.translate(text)
        except TranslationException:
            return text

    def get_xml_string(self, file_information: FileInformation, video: Video) -> str:
        movie = Element('movie')
        SubElement(movie, 'title').text = self.translate(video.title)
        SubElement(movie, 'set').text = None
        SubElement(movie, 'rating').text = str(0)
        SubElement(movie, 'studio').text = video.studio
        SubElement(movie, 'year').text = str(video.release_date.year) if video.release_date else None
        SubElement(movie, 'outline').text = video.outline
        SubElement(movie, 'plot').text = video.outline
        SubElement(movie, 'runtime').text = str(video.runtime) if video.runtime else None
        SubElement(movie, 'premiered').text = video.release_date.strftime('%Y-%m-%d') if video.release_date else None
        SubElement(movie, 'release').text = video.release_date.strftime('%Y-%m-%d') if video.release_date else None
        SubElement(movie, 'maker').text = video.studio
        SubElement(movie, 'director').text = video.director
        SubElement(movie, 'num').text = video.number

        for keyword in video.keywords:
            SubElement(movie, 'genre').text = keyword

        for index, star in enumerate(video.stars):
            actor = SubElement(movie, 'actor')
            SubElement(actor, 'name').text = star.name
            SubElement(actor, 'role').text = star.name
            SubElement(actor, 'thumb').text = star.avatar_url
            SubElement(actor, 'order').text = str(index)

        return minidom.parseString(tostring(movie, 'UTF-8')).toprettyxml(indent=' ' * 2)
