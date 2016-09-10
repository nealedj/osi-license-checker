import re

from .. import license_matcher
from .base import BaseProcessor

URL_DATA_PATTERN = re.compile(r'(?:pypi.python.org\/)?pypi\/([\w\-\_]+)')
JSON_DATA_PATTERN = 'http://pypi.python.org/pypi/{0.repo}/json'
JSON_DATA_PATTERN_WITH_VERSION = 'http://pypi.python.org/pypi/{0.repo}/{0.version}/json'


class PyPiProcessor(BaseProcessor):
    name = 'pypi'

    def __init__(self, url=None, repo=None, version=None):
        self.url = url
        self.repo = repo or self.extract_url_data()[0]
        self.version = version

    def extract_url_data(self):
        match = URL_DATA_PATTERN.match(self.url)
        return match.groups()

    @classmethod
    def is_match(cls, url):
        return URL_DATA_PATTERN.match(url)

    def get_license(self):
        repo_info, data_url = self.get_repo_info()

        if repo_info:
            license = repo_info.get('license')

            if not license:
                license = self.get_license_from_classifiers(repo_info)
                data_url += ' (from classifiers)'
        else:
            license = None

        return license, data_url

    def get_repo_info(self):
        file_data = None

        if self.version:
            # try and get the version-specific info
            data_url = JSON_DATA_PATTERN_WITH_VERSION.format(self)
            file_data = self.get_file_data(
                data_url,
                parse_json=True
            )

        if not file_data:
            data_url = JSON_DATA_PATTERN.format(self)
            file_data = self.get_file_data(
                data_url,
                parse_json=True
            )

        if file_data:
            return file_data.get('info'), data_url

    def get_license_from_classifiers(self, repo_info):
        classifiers = repo_info['classifiers']

        pattern = r"License :: OSI Approved :: ([\w\s]*)"
        for classifier in classifiers:
            match = re.search(pattern, classifier)
            if match and match.groups():
                return match.groups()[0]
