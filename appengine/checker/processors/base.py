from contextlib import closing
import json
import urllib2

from .. import license_matcher


class BaseProcessor(object):
    name = "unspecified"

    @classmethod
    def get_file_data(cls, file_url, parse_json=None):
        try:
            with closing(urllib2.urlopen(file_url)) as file_handle:
                file_data = file_handle.read()
        except urllib2.HTTPError:
            file_data = ''

        if file_data and parse_json:
            return json.loads(file_data)

        return file_data

    def get_license_from_license_file(self, file_url):
        file_data = self.get_file_data(file_url)

        return license_matcher.match(file_data)
