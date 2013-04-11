# -*- coding: utf-8 -*-

from urllib import urlencode

from grab import Grab, UploadFile
from time import sleep


DEBUG = False


class AntiGateError(Exception):
    """
    Raised when execution status not is 200
    """


class AntiGate(object):

    def __init__(self, key, filename):
        self.g = Grab()
        self.g.setup(hammer_mode=True,
                     hammer_timeouts=((60, 70), (80, 90), (100, 110)))
        self.key = key
        self.captcha_id = None

        self.run(filename)

    def _get_input_url(self):
        if DEBUG:
            return 'http://127.0.0.1:8000/in.php'
        return 'http://antigate.com/in.php'

    def _get_result_url(self):
        params = urlencode({
            'key': self.key, 'action': 'get', 'id': self.captcha_id
        })
        if DEBUG:
            return 'http://127.0.0.1:8000/res.php?%s' % params
        return 'http://antigate.com/res.php?%s' % params

    def _send(self, filename):
        self.g.setup(multipart_post={
            'key': self.key,
            'file': UploadFile(filename)
        })
        self.g.go(self._get_input_url())
        if self.g.response.code == 200:
            body = self.g.response.body.split('|')
            if len(body) == 2:
                self.captcha_id = int(body[1])
                return self.captcha_id
            raise AntiGateError(body[0])
        else:
            raise AntiGateError(
                '%s %s' % (self.g.response.code, self.g.response.body)
            )

    def send(self, filename):
        while True:
            try:
                self._send(filename)
            except AntiGateError, msg:
                if str(msg) != 'ERROR_NO_SLOT_AVAILABLE':
                    raise AntiGateError(msg)
            else:
                break

    def _get(self):
        self.g.go(self._get_result_url())
        body = self.g.response.body.split('|')
        if len(body) == 2:
            self.captcha_key = body[1]
            return self.captcha_key
        raise AntiGateError(body[0])

    def get(self):
        while True:
            try:
                return self._get()
            except AntiGateError, msg:
                if str(msg) == 'CAPCHA_NOT_READY':
                    sleep(10)
                else:
                    raise AntiGateError(msg)

    def run(self, filename):
        self.send(filename)
        self.get()

    def __str__(self):
        return self.captcha_key
