# -*- encoding: utf-8 -*-

try:
    from urllib2 import Request, urlopen
    from urllib import urlencode
except ImportError:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode

import base64

from six import PY3


class Http(object):
    def __init__(self, **config):
        self.u = None
        self.r = None
        self.conf = {}
        self.config = config

    def get_response_body(self):
        if PY3 is True:
            return self.r.decode('utf-8')
        return self.r

    @staticmethod
    def url_encode(data):
        if PY3 is True:
            return urlencode(data).encode('ascii')
        return urlencode(data)

    def request(self, url):
        if self.conf.get('post'):
            req = Request(
                url, self.url_encode(self.conf.get('post')))
        elif self.conf.get('multipart_post'):
            filename = self.conf['multipart_post']['file']
            fp = open(filename, 'rb').read()
            self.conf['multipart_post']['method'] = 'base64'
            self.conf['multipart_post']['body'] = base64.b64encode(fp)

            req = Request(
                url, self.url_encode(self.conf.get('multipart_post')))
        else:
            req = Request(url, **self.config)
        self.u = urlopen(req)
        self.r = self.u.read()
        return self.u.getcode(), self.r

    def setup(self, **kwargs):
        self.conf.update(kwargs)

    @staticmethod
    def upload(filename):
        return filename

    def reset(self):
        self.conf = {}
        self.u = None
        self.r = None
