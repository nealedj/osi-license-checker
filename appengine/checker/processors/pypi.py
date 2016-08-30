import re

from .. import license_matcher
from .base import BaseProcessor

URL_DATA_PATTERN = re.compile(r'pypi.python.org\/pypi\/([\w\-\_]+)')
JSON_DATA_PATTERN = 'http://pypi.python.org/pypi/{0.repo}/json'


class PyPiProcessor(BaseProcessor):
    name = 'pypi'

    def __init__(self, url):
        self.url = url
        self.repo = self.extract_url_data()[0]

    def extract_url_data(self):
        match = URL_DATA_PATTERN.match(self.url)
        return match.groups()

    @classmethod
    def is_match(cls, url):
        return URL_DATA_PATTERN.match(url)

    def get_license(self):
        repo_info = self.get_file_data(JSON_DATA_PATTERN.format(self), parse_json=True)

        classifiers = repo_info['info']['classifiers']

        pattern = r"License :: OSI Approved :: ([\w\s]*)"
        for classifier in classifiers:
            match = re.search(pattern, classifier)
            if match and match.groups():
                return match.groups()[0]
