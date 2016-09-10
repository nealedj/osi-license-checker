import re

from .. import license_matcher
from .base import BaseProcessor

URL_DATA_PATTERN = re.compile(r'(pypi.python.org\/)?pypi\/([\w\-\_]+)')
JSON_DATA_PATTERN = 'http://pypi.python.org/pypi/{0.repo}/json'


class PyPiProcessor(BaseProcessor):
    name = 'pypi'

    def __init__(self, url):
        self.url = url
        self.repo = self.extract_url_data()[1]

    def extract_url_data(self):
        match = URL_DATA_PATTERN.match(self.url)
        return match.groups()

    @classmethod
    def is_match(cls, url):
        return URL_DATA_PATTERN.match(url)

    def get_license(self):
        data_url = JSON_DATA_PATTERN.format(self)

        repo_info = self.get_file_data(
            data_url,
            parse_json=True
        )

        return repo_info['info'].get('license'), data_url
