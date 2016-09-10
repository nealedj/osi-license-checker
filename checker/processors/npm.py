import re

from .. import license_matcher
from .base import BaseProcessor

URL_DATA_PATTERN = re.compile(r'(www.)?npm(js)?(.com)?\/(package\/)?([\w\-\_]+)')
JSON_DATA_PATTERN = 'http://registry.npmjs.org/{0.repo}/{0.version}'


class NpmProcessor(BaseProcessor):
    name = 'npm'

    def __init__(self, url=None, repo=None, version=None):
        self.url = url
        self.repo = repo or self.extract_url_data()[4]
        self.version = version or 'latest'

    def extract_url_data(self):
        match = URL_DATA_PATTERN.search(self.url)
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

        return repo_info.get('license'), data_url
