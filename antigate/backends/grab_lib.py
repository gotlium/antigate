# -*- encoding: utf-8 -*-

from grab import Grab, UploadFile
from six import PY2


class Http(object):
    def __init__(self, **config):
        print("> GrabLib")
        self.grab = Grab(**(config or {}))

    def get_response_body(self):
        if PY2 is True:
            return self.grab.response.body
        return self.grab.response.body.decode('utf-8')

    def request(self, url):
        self.grab.go(url)
        return self.grab.response.code, self.get_response_body()

    def setup(self, *args, **kwargs):
        self.grab.setup(*args, **kwargs)

    def upload(self, filename):
        return UploadFile(filename)

    def reset(self):
        self.grab.reset()
