from shutil import move
from typing import Optional
from pathlib import Path
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom

from jmm.utilities.metadata import Video
from jmm.utilities.file_information import FileInformation
from jmm.utilities.translator import Translator
from jmm.utilities.translator import TranslationException

class FileManager:
    def __init__(self, file_path_pattern: str, mode: str, translator: Optional[Translator] = None):
        self.mode = mode
        self.file_path_pattern = file_path_pattern
        self.translator = translator

    def manager(self, file_information: FileInformation, video: Video) -> Path:
        format_arguments = {
            'suffix': file_information.file_path.suffix,
            'number': video.number.upper(),
            'star': video.stars[0].name if video.stars else 'unknown',
            'subtitle': '-C' if file_information.has_chinese_subtitle else '',
            'series': video.series or 'unknown',
            'studio': video.studio or 'unknown'
        }

        media_file_path = Path(self.file_path_pattern.format(**format_arguments))
        fanart_file_path = media_file_path.with_name(media_file_path.stem + '-fanart').with_suffix('.jpg')
        poster_file_path = media_file_path.with_name(media_file_path.stem + '-poster').with_suffix('.jpg')
        nfo_file_path = media_file_path.with_suffix('.nfo')

        media_file_path.parent.mkdir(exist_ok=True, parents=True)
        move(file_information.file_path, media_file_path)

        with open(nfo_file_path, 'w', encoding='utf8') as file:
            file.write(self.get_xml_string(video))

        if video.fanart:
            video.fanart.save(fanart_file_path)

        if video.poster:
            video.poster.save(poster_file_path)

        return media_file_path

    def translate(self, text: Optional[str]) -> str:
        if text is None:
            return ''

        if not self.translator:
            return text

        try:
            return self.translator.translate(text)
        except TranslationException:
            return text

    def get_xml_string(self, video: Video) -> str:
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
