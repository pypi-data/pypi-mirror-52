# -*- coding: utf-8 -*-
from .misc import (
    Context,
)

from .exceptions import (
    BamboraError,
    AuthorizationError,
    AuthenticationError,
    NotFoundError,
    APIError
)
from .base_objects import (
    RESTManager,
    RESTObject,
    Scoped
)

class Card(RESTObject):
    _id_attr = 'card_id'


class Cards(RESTManager):
    _path = 'cards'
    _obj_cls = Card
    _map_data = {
        'get': 'card',
        'list': 'card',
        'put': 'validation',
        'create': 'validation',
    }
    _get_first = True


class Profile(RESTObject):
    _id_attr = 'customer_code'
    _managers = [
        ('cards', Cards),
    ]


class Profiles(RESTManager):
    _path = 'profiles' 
    _obj_cls = Profile
    _passcode_name = 'payment_profile_passcode'


class Payment(RESTObject):
    _id_attr = 'id'

class Payments(RESTManager):
    _path = 'payments'
    _obj_cls = Payment
    _passcode_name = 'payment_passcode'

class Token(RESTObject):
    _id_attr = None


class Tokens(RESTManager):
    _path = 'scripts/tokenization/tokens'
    _obj_cls = Token
    _passcode_name = None


class Report(RESTObject):
    _id_attr = None


class Reports(RESTManager):
    _path = 'reports'
    _obj_cls = Report
    _map_data = {
        'list': 'records'
    }
    _passcode_name = 'report_passcode'


class Bambora(RESTObject):
    _path = 'v1'

    _managers = [
        ('profiles', Scoped(Profiles, 'v1')),
        ('payments', Scoped(Payments, 'v1')),
        ('reports', Scoped(Reports, 'v1')),
        ('tokens', Tokens),
    ]

    def __init__(self, context):
        self.context = Context(context)
        self._url = context['url']
        super(Bambora, self).__init__(self, context)

    def get_path(self):
        return self._url

    def get_passcode_name(self):
        return None
