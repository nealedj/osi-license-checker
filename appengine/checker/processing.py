from . import processors

PROCESSORS = {
    'github': processors.GitHubProcessor,
    'pypi': processors.PyPiProcessor,
    'npm': processors.NpmProcessor
}


class Processor(object):
    def __init__(self, url):
        self.url = url

    def get_processor(self):
        for processor in PROCESSORS.values():
            if processor.is_match(self.url):
                return processor

    def get_license(self):
        processor_cls = self.get_processor()

        data = {
            'type': 'unknown',
            'license': None
        }

        if processor_cls:
            processor = processor_cls(self.url)
            data['type'] = processor.name
            data['license'] = processor.get_license()

        return data
