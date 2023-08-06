# -*- coding: utf-8 -*-
from .exceptions import (
    BamboraError,
    AuthorizationError,
    AuthenticationError,
    NotFoundError,
    APIError
)


class RESTObject(object):
    _id_attr = 'id'
    _passcode_name = None
    _managers = None

    def __init__(self, manager, attrs):
        self._attrs = attrs
        self._manager = manager
        self.context = self._manager.context
        self._create_managers()

    def __getattr__(self, name):
        return self._attrs[name]

    def _create_managers(self):
        if not hasattr(self, '_managers') or not self._managers:
            return

        for name, klass in self._managers:
            manager = klass(self._manager.context, parent=self)
            setattr(self, name, manager)    

    def get_id(self):
        if self._id_attr is None:
            return None
        return getattr(self, self._id_attr)

    def get_path(self):
        return "%s/%s" % (self._manager.get_path(), self.get_id())

    def get_passcode_name(self):
        if self._passcode_name is not None:
            return self._passcode_name
        return self._manager.get_passcode_name()

    def delete(self):

        data = self.context.call(
            'DELETE',
            self.get_path(),
            self.get_passcode_name(),
            {}
        )

        manager = self._manager

        rdata = data
        if hasattr(manager, '_map_data') and manager._map_data.get('delete'):
            rdata = data[manager._map_data.get('delete')]

        return rdata


class RESTManager(object):
    _path = None
    _obj_cls = None
    _parent = None

    def __init__(self, context, parent=None):
        self.context = context
        self._parent = parent

    def get(self, id):
        attrs = {}
        attrs[self._obj_cls._id_attr] = id
        obj = self._obj_cls(self, attrs)
        data = self.context.call(
            'GET',
            obj.get_path(),
            obj.get_passcode_name(),
            {}
        )

        rdata = data
        if hasattr(self, '_map_data') and self._map_data.get('get'):
            rdata = data[self._map_data.get('get')]
            if self._get_first:
                rdata = rdata[0]

        real_obj = self._obj_cls(self, data)
        real_obj._get_data = data
        return real_obj

    def create(self, attrs):
        data = self.context.call(
            'POST',
            self.get_path(),
            self.get_passcode_name(),
            attrs
        )

        rdata = data
        if hasattr(self, '_map_data') and self._map_data.get('create'):
            rdata = data[self._map_data.get('create')]

        if self._obj_cls._id_attr:
            obj = self.get(rdata[self._obj_cls._id_attr])
            obj._create_data = data
        else:
            obj = self._obj_cls(self, rdata)

        return obj

    
    def list(self, params=None):
        if params is None:
            method = 'GET'
        else:
            method = 'POST'

        data = self.context.call(
            method,
            self.get_path(),
            self.get_passcode_name(),
            params or {}
        )

        rdata = data
        if hasattr(self, '_map_data') and self._map_data.get('list'):
            rdata = rdata[self._map_data.get('list')]

        objs = []

        for obj in rdata:
            new_obj = self._obj_cls(self, obj)
            new_obj._orig_response = data
            objs.append(new_obj)

        return objs

    def get_path(self):
        return "%s/%s" % (self._parent.get_path(), self._path)

    def get_passcode_name(self):
        if hasattr(self, '_passcode_name') and self._passcode_name is not None:
            return self._passcode_name
        return self._parent.get_passcode_name()


class Scoped(object):
    def __init__(self, model, namespace):
        self.namespace = namespace
        self.model = model

    def __call__(self, *args, **kwargs):
        obj = self.model(*args, **kwargs)
        obj._path = "%s/%s" % (self.namespace, obj._path)
        return obj
