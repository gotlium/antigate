# -*- coding: utf-8 -*-

from logging import getLogger
from datetime import datetime

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from xmltodict import parse
from sys import exc_info
from time import sleep

from grab import Grab, UploadFile


DEBUG = False


class AntiGateError(Exception):
    """
    API errors
    """


class AntiGate(object):
    def __init__(self, key, filename='', auto_run=True,
                 grab_config=None, send_config=None,
                 domain='antigate.com'):
        self.g = Grab()
        if grab_config:
            self.g.setup(**grab_config)
        self.key = key
        self.captcha_id = None
        self.captcha_key = None
        self.send_config = send_config
        self.domain = domain
        self.logger = getLogger(__name__)

        if auto_run and filename:
            self.run(filename)

    def _get_domain(self, path):
        if DEBUG:
            return 'http://127.0.0.1:8000/%s' % path
        return 'http://%s/%s' % (self.domain, path)

    def _get_input_url(self):
        return self._get_domain('in.php')

    def _update_params(self, defaults, additional):
        if additional is not None and additional:
            defaults.update(additional)
        return defaults

    def _get_build_url(self, action='get', data=None):
        params = urlencode(self._update_params(
            {'key': self.key, 'action': action}, data
        ))
        return self._get_domain('res.php?%s' % params)

    def _get_result_url(self, action='get', captcha_id=None):
        return self._get_build_url(action, {
            'id': captcha_id and captcha_id or self.captcha_id})

    def _get_balance_url(self):
        return self._get_build_url('getbalance')

    def _get_stats_url(self):
        return self._get_build_url('getstats', {
            'date': datetime.now().strftime('%Y-%m-%d')})

    def _body(self, key):
        body = self.g.response.body.split('|')
        if len(body) != 2 or body[0] != 'OK':
            raise AntiGateError(body[0])
        setattr(self, key, body[1])
        return body[1]

    def _response_to_dict(self):
        return parse(self.g.response.body.lower())['response']

    def _go(self, url, err):
        self.g.go(url)
        if self.g.response.code != 200:
            raise AntiGateError('Code: %d\nMessage: %s\nBody: %s' % (
                self.g.response.code, err, self.g.response.body
            ))

    def _send(self, filename):
        self.g.setup(multipart_post=self._update_params(
            {'key': self.key, 'file': UploadFile(filename)}, self.send_config))
        self._go(self._get_input_url(), 'Can not send captcha')
        return self._body('captcha_id')

    def send(self, filename):
        self.logger.debug('Sending captcha')
        while True:
            try:
                return self._send(filename)
            except AntiGateError:
                msg = exc_info()[1]
                self.logger.debug(msg)
                if str(msg) != 'ERROR_NO_SLOT_AVAILABLE':
                    raise AntiGateError(msg)

    def _get(self, captcha_id=None):
        self.g.reset()
        self._go(self._get_result_url(captcha_id=captcha_id),
                 'Can not get captcha')
        return self._body('captcha_key')

    def get(self, captcha_id=None):
        self.logger.debug('Fetching result')
        sleep(10)
        while True:
            try:
                return self._get(captcha_id)
            except AntiGateError:
                msg = exc_info()[1]
                self.logger.debug(msg)
                if str(msg) == 'CAPCHA_NOT_READY':
                    sleep(5)
                else:
                    raise AntiGateError(msg)

    def _get_multi(self, ids):
        self._go(self._get_build_url(data={
            'ids': ','.join(map(str, ids))}), 'Can not get result')
        return self.g.response.body.split('|')

    def get_multi(self, ids):
        results = self._get_multi(ids)
        while 'CAPCHA_NOT_READY' in results:
            sleep(10)
            results = self._get_multi(ids)
        return results

    def abuse(self):
        self._go(self._get_result_url('reportbad'), 'Can not send report')
        return True

    def balance(self):
        self._go(self._get_balance_url(), 'Can not get balance')
        return float(self.g.response.body)

    def stats(self):
        self._go(self._get_stats_url(), 'Can not get stats')
        return [s for s in self._response_to_dict()['stats']]

    def load(self):
        self._go(self._get_domain('load.php'), 'Can not get loads')
        return self._response_to_dict()

    def run(self, filename):
        self.send(filename)
        self.get()

    def __str__(self):
        return self.captcha_key
