# -*- coding: utf-8 -*-

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from datetime import datetime
from logging import getLogger
from base64 import b64encode
from sys import exc_info
from time import sleep
from os import getenv
from re import match

from six import PY3

try:
    from antigate.backends.grab_lib import Http
except ImportError:
    try:
        from antigate.backends.requests_lib import Http
    except ImportError:
        from antigate.backends.urllib_lib import Http

if getenv('ANTIGATE_HTTP_BACKEND'):
    import importlib

    Http = importlib.import_module(getenv('ANTIGATE_HTTP_BACKEND')).Http


__all__ = ('AntiGateError', 'AntiGate', 'AntiCaptcha')


class AntiGateError(Exception):
    """
    API errors
    """

    def __init__(self, *args, **kwargs):
        super(AntiGateError, self).__init__(*args, **kwargs)
        if len(args) > 0 and args[0] and args[0] != 'CAPCHA_NOT_READY':
            getLogger(__name__).error(args[0])


class AntiGate(object):
    __slots__ = [
        'http', 'domain', 'api_key', 'captcha_id', 'captcha_result',
        'send_config', 'logger', 'check_interval'
    ]

    def __init__(self, api_key, captcha_file=None, auto_run=True,
                 grab_config=None, send_config=None,
                 domain='antigate.com', check_interval=10):

        self.http = Http(**(grab_config or {}))
        self.domain = domain
        self.api_key = api_key
        self.captcha_id = None
        self.captcha_result = None
        self.send_config = send_config
        self.logger = getLogger(__name__)
        self.check_interval = check_interval

        if auto_run and captcha_file:
            self.run(captcha_file)

    @staticmethod
    def _update_params(defaults, additional):
        if additional is not None and additional:
            defaults.update(additional)
        return defaults

    @staticmethod
    def _is_base64(s):
        is_base64 = False
        if len(s) % 4 == 0:
            try:
                is_base64 = match('^[A-Za-z0-9+/]+[=]{0,2}$', s)
            except TypeError:
                is_base64 = match(b'^[A-Za-z0-9+/]+[=]{0,2}$', s)
        return is_base64 and True

    @staticmethod
    def _is_binary(s):
        try:
            is_binary = '\0' in s
        except TypeError:
            is_binary = b'\0' in s
        return is_binary

    def _get_domain(self, path):
        return 'http://%s/%s' % (self.domain, path)

    def _get_input_url(self):
        return self._get_domain('in.php')

    def _build_url(self, action='get', data=None):
        params = urlencode(self._update_params(
            {'key': self.api_key, 'action': action}, data
        ))
        return self._get_domain('res.php?%s' % params)

    def _get_result_url(self, action='get', captcha_id=None):
        return self._build_url(action, {
            'id': captcha_id or self.captcha_id
        })

    def _get_balance_url(self):
        return self._build_url('getbalance')

    def _get_stats_url(self):
        return self._build_url('getstats', {
            'date': datetime.now().strftime('%Y-%m-%d')
        })

    def _get_response_body(self):
        return self.http.get_response_body()

    def _get_response(self, key=None):
        body = self._get_response_body().split('|')
        if len(body) != 2 or body[0] != 'OK':
            raise AntiGateError(body[0])
        if key is not None:
            setattr(self, key, body[1])
        return body[1]

    def _response_to_dict(self):
        from xmltodict import parse

        return parse(self._get_response_body().lower()).get('response', {})

    def _request(self, url, err):
        code, response = self.http.request(url)
        if code != 200:
            raise AntiGateError('Code: %d\nMessage: %s\nBody: %s' % (
                code, err, response
            ))

    def _send(self, captcha_file):
        is_base64 = self._is_base64(captcha_file)
        is_binary = self._is_binary(captcha_file)

        if is_binary or is_base64:
            body = b64encode(captcha_file) if not is_base64 else captcha_file
            if PY3 is True:
                body = body.decode('utf-8')
            self.http.setup(post=self._update_params({
                'method': 'base64', 'key': self.api_key, 'body': body},
                self.send_config
            ))
        else:
            self.http.setup(multipart_post=self._update_params({
                'method': 'post', 'key': self.api_key,
                'file': self.http.upload(captcha_file)},
                self.send_config
            ))
        self._request(self._get_input_url(), 'Can not send captcha')
        return self._get_response('captcha_id')

    def _get(self, captcha_id=None):
        self.http.reset()
        self._request(
            self._get_result_url(captcha_id=captcha_id), 'Can not get captcha')
        return self._get_response('captcha_result')

    def _get_multi(self, ids):
        self._request(self._build_url(data={
            'ids': ','.join(map(str, ids))}), 'Can not get result')
        return self._get_response_body().split('|')

    def send(self, captcha_file):
        self.logger.debug('Sending captcha')
        while True:
            try:
                return self._send(captcha_file)
            except AntiGateError:
                msg = exc_info()[1]
                if str(msg) != 'ERROR_NO_SLOT_AVAILABLE':
                    raise AntiGateError(msg)
                sleep(0.5)

    def get(self, captcha_id=None):
        self.logger.debug('Fetching result')
        sleep(self.check_interval)
        while True:
            try:
                return self._get(captcha_id)
            except AntiGateError:
                msg = exc_info()[1]
                if str(msg) == 'CAPCHA_NOT_READY':
                    sleep(self.check_interval / 2.0)
                else:
                    raise AntiGateError(msg)

    def get_multi(self, ids):
        self.logger.debug('Fetching multi result')
        results = self._get_multi(ids)
        while 'CAPCHA_NOT_READY' in results:
            sleep(self.check_interval)
            results = self._get_multi(ids)
        return results

    def abuse(self):
        self._request(self._get_result_url('reportbad'), 'Can not send report')
        return True

    def balance(self):
        self._request(self._get_balance_url(), 'Can not get balance')
        return float(self._get_response_body())

    def stats(self):
        self._request(self._get_stats_url(), 'Can not get stats')
        return [s for s in self._response_to_dict().get('stats', [])]

    def load(self):
        self._request(self._get_domain('load.php'), 'Can not get loads')
        return self._response_to_dict()

    def run(self, captcha_file):
        self.send(captcha_file)
        self.get()

    def __len__(self):
        if self.captcha_result:
            return len(self.captcha_result)

    def __str__(self):
        return self.captcha_result


class AntiCaptcha(AntiGate):
    def __init__(self, *args, **kwargs):
        kwargs['domain'] = 'anti-captcha.com'
        super(AntiCaptcha, self).__init__(*args, **kwargs)
