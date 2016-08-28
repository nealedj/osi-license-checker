from contextlib import closing
import json
import re
import urllib2

from .. import license_matcher
from .base import BaseProcessor

URL_DATA_PATTERN = re.compile(r'github.com\/([\w\-\_]+)\/([\w\-\_]+)')
CONTENTS_URL = 'https://api.github.com/repos/{0.username}/{0.repo}/contents'


class GitHubProcessor(BaseProcessor):
    name = 'github'

    def __init__(self, url):
        self.url = url
        self.username, self.repo = self.extract_url_data()

    def extract_url_data(self):
        match = URL_DATA_PATTERN.match(self.url)
        return match.groups()

    @classmethod
    def is_match(cls, url):
        return URL_DATA_PATTERN.match(url)

    def get_license(self):
        file_list = self.get_file_list()

        license = None
        if 'setup.py' in file_list:
            license = self.get_license_from_setup_py(file_list['setup.py'])

        if 'LICENSE' in file_list and not license:
            license = self.get_license_from_license(file_list['LICENSE'])

        return license

    def get_file_list(self):
        contents_url = CONTENTS_URL.format(self)

        try:
            with closing(urllib2.urlopen(contents_url)) as contents_file:
                file_data = contents_file.read()
        except urllib2.HTTPError:
            return {}

        contents = json.loads(file_data)
        return {f['name']: f['download_url'] for f in contents}

    def get_license_from_setup_py(self, download_url):
        # TODO: move to base
        with closing(urllib2.urlopen(download_url)) as setup_file:
            file_data = setup_file.read()

        pattern = r"License :: OSI Approved :: (\w*)"
        match = re.search(pattern, file_data)
        return match and match.groups()[0]

    def get_license_from_license(self, download_url):
        with closing(urllib2.urlopen(download_url)) as license_file:
            file_data = license_file.read()

        return license_matcher.match(file_data)
