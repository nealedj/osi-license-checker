import json
import webapp2
from webapp2_extras.routes import RedirectRoute

from checker import processing


class MainHandler(webapp2.RequestHandler):
    def get(self, url=None):
        processor = processing.Processor(url)
        license = processor.get_license()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(license))

routes = [
    RedirectRoute(
        '/check/<url:(.+)>',
        MainHandler,
        name='home',
        strict_slash=True
    ),
]

try:
    with open('secret_key') as key_f:
        key = key_f.read()
except:
    raise Exception('Run generate_secret_key.sh')

webapp2_config = {
    'webapp2_extras.sessions': {
        'secret_key': key
    },
}

application = webapp2.WSGIApplication(
    debug=True,  # TODO: detect
    config=webapp2_config,
    routes=routes
)
