# -*- coding: utf-8 -*-

from urllib import urlencode
from time import sleep
from datetime import datetime
from xmltodict import parse

from grab import Grab, UploadFile


DEBUG = False


class AntiGateError(Exception):
    """
    Raised when execution status not is 200
    """


class AntiGate(object):

    def __init__(self, key, filename):
        self.g = Grab()
        self.key = key
        self.captcha_id = None

        self.run(filename)

    def _get_input_url(self):
        if DEBUG:
            return 'http://127.0.0.1:8000/in.php'
        return 'http://antigate.com/in.php'

    def _get_build_url(self, action='get', data=None):
        default = {'key': self.key, 'action': action}
        if data is not None:
            default.update(data)
        params = urlencode(default)
        if DEBUG:
            return 'http://127.0.0.1:8000/res.php?%s' % params
        return 'http://antigate.com/res.php?%s' % params

    def _get_result_url(self, action='get'):
        return self._get_build_url(action, {'id': self.captcha_id})

    def _get_balance_url(self):
        return self._get_build_url('getbalance')

    def _get_stats_url(self):
        return self._get_build_url('getstats', {
            'date': datetime.now().strftime('%Y-%m-%d')})

    def _check_status_code(self, message):
        if self.g.response.code != 200:
            raise AntiGateError(message)

    def _send(self, filename):
        self.g.setup(multipart_post={
            'key': self.key,
            'file': UploadFile(filename)
        })
        self.g.go(self._get_input_url())
        self._check_status_code(
            '%s %s' % (self.g.response.code, self.g.response.body))
        body = self.g.response.body.split('|')
        if len(body) == 2:
            self.captcha_id = int(body[1])
            return self.captcha_id
        raise AntiGateError(body[0])

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
        self.g.reset()
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

    def abuse(self):
        self.g.go(self._get_result_url('reportbad'))
        self._check_status_code('Can not send report')
        return True

    def balance(self):
        self.g.go(self._get_balance_url())
        self._check_status_code('Can not get balance')
        return float(self.g.response.body)

    def stats(self):
        self.g.go(self._get_stats_url())
        self._check_status_code('Can not get stats')
        results = parse(self.g.response.body)
        return [s for s in results['response']['stats']]

    def run(self, filename):
        self.send(filename)
        self.get()

    def __str__(self):
        return self.captcha_key
