# -*- encoding: utf-8 -*-

import requests


class Http(object):
    def __init__(self, **config):
        self.r = None
        self.conf = {}
        self.config = config

    def get_response_body(self):
        if self.r:
            return self.r.text

    def request(self, url):
        if self.conf.get('post'):
            self.r = requests.post(
                url, data=self.conf.get('post'), **self.config)
        elif self.conf.get('multipart_post'):
            filename = self.conf['multipart_post'].pop('file', None)
            files = {}

            if filename is not None:
                files = {
                    "file": open(filename, 'rb'),
                }

            self.r = requests.post(
                url, data=self.conf.get('multipart_post'),
                files=files, **self.config
            )
        else:
            self.r = requests.get(url, **self.config)
        return self.r.status_code, self.r.text

    def setup(self, **kwargs):
        self.conf.update(kwargs)

    @staticmethod
    def upload(filename):
        return filename

    def reset(self):
        self.conf = {}
        self.r = None
