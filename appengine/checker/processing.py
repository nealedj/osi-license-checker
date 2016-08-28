from . import processors

PROCESSORS = {
    'github': processors.GitHubProcessor
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
        processor = processor_cls(self.url)
        return {
            'type': processor.name,
            'license': processor.get_license()
        }
