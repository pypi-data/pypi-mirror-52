# -*- coding: utf-8 -*-


class BamboraError(Exception):
    def __init__(self, attrs):
        self._attrs = attrs
        if 'message' in self._attrs:
            self.message = self._attrs['message']
        else:
            self.message = 'Unexpected Error'

    def __getattr__(self, name):
        return self._attrs[name]

    def __repr__(self):
        return str(self._attrs)


class AuthenticationError(BamboraError):
    pass


class AuthorizationError(BamboraError):
    pass


class NotFoundError(BamboraError):
    pass


class APIError(BamboraError):
    pass
