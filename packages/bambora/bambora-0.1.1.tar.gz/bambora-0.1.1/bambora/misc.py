# -*- coding: utf-8 -*-
import base64
import requests
import logging
from requests.auth import AuthBase

from .exceptions import (
    BamboraError,
    AuthorizationError,
    AuthenticationError,
    NotFoundError,
    APIError
)


log = logging.getLogger(__name__)


class BamboraAuth(AuthBase):
    def __init__(self, merchant_id, passcode):
        self.merchant_id = merchant_id
        self.passcode = passcode

    def __call__(self, req):
        key = "%s:%s" % (self.merchant_id, self.passcode)
        auth = base64.b64encode(key.encode('utf-8')).decode('utf-8')
        b_passcode = 'Passcode %s' % auth
        req.headers['Authorization'] = b_passcode
        return req


class Context(object):

    def __init__(self, attrs):
        self._attrs = attrs

    def __getattr__(self, name):
        return self._attrs[name]

    def call(self, method, url, passcode, data, headers=None):
        kwargs = {}

        if passcode:

            kwargs['auth'] = BamboraAuth(
                self.merchant_id,
                self.codes[passcode]
            )

        if headers is not None:
            kwargs['headers'] = headers

        log.info('Making a request to %s with %s method' % (url, method))

        if method == 'GET':
            req = requests.get(url, **kwargs)
        elif method == 'POST':
            req = requests.post(url, json=data, **kwargs)
        elif method == 'DELETE':
            req = requests.delete(url, json=data, **kwargs)

        if req.status_code == 200:
            data = req.json()
            return data
        elif req.status_code == 401:
            raise AuthenticationError(req.json())
        elif req.status_code == 403:
            raise AuthorizationError(req.json())
        elif req.status_code == 404:
            raise NotFoundError('Not found')
        else:
            raise APIError(req.json())
