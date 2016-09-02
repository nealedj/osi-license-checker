import re

from .. import license_matcher
from .base import BaseProcessor

URL_DATA_PATTERN = re.compile(r'(www.)?npmjs.com\/package\/([\w\-\_]+)')
JSON_DATA_PATTERN = 'http://registry.npmjs.org/{0.repo}/latest'


class NpmProcessor(BaseProcessor):
    name = 'npm'

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
        repo_info = self.get_file_data(
            JSON_DATA_PATTERN.format(self),
            parse_json=True
        )

        return repo_info.get('license')
