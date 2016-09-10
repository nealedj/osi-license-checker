import re
import urllib2

from .base import BaseProcessor

URL_DATA_PATTERN = re.compile(r'github(?:.com)?\/([\w\-\_]+)\/([\w\-\_]+)(?:\.git)?')
CONTENTS_URL = 'https://api.github.com/repos/{0.username}/{0.repo}/contents'


class GitHubProcessor(BaseProcessor):
    name = 'github'

    def __init__(self, url):
        self.url = url
        self.username, self.repo = self.extract_url_data()

    def extract_url_data(self):
        return URL_DATA_PATTERN.search(self.url).groups()

    @classmethod
    def is_match(cls, url):
        return URL_DATA_PATTERN.match(url)

    def get_license(self):
        file_list = self.get_file_list()

        license = None
        if 'setup.py' in file_list:
            license = self.get_license_from_setup_py(file_list['setup.py'])
            license_found_in = file_list['setup.py']

        if 'LICENSE' in file_list and not license:
            license = self.get_license_from_license_file(file_list['LICENSE'])
            license_found_in = file_list['LICENSE']

        return license, license_found_in

    def get_file_list(self):
        contents_url = CONTENTS_URL.format(self)

        contents = self.get_file_data(contents_url, parse_json=True)
        return {f['name']: f['download_url'] for f in contents}

    def get_license_from_setup_py(self, download_url):
        file_data = self.get_file_data(download_url)

        pattern = r"License :: OSI Approved :: (\w*)"
        match = re.search(pattern, file_data)
        return match and match.groups()[0]
