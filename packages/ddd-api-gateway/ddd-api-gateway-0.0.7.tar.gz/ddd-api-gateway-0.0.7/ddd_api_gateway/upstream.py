# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
import uuid
from urllib.parse import urlparse
from ddd_base import Entity
from .prototype import Prototype


class Upstream(Entity, Prototype):

    def __init__(self, name, endpoints):
        super(Upstream, self).__init__()
        self.name = name
        self.endpoints = endpoints

    @property
    def host(self):
        if self.endpoints is not None and len(self.endpoints) > 0:
            endpoint = self.endpoints[0]
            if endpoint.startswith('http') or endpoint.startswith('https'):
                return urlparse(endpoint).hostname
            else:
                return urlparse('http://{}'.format(endpoint)).hostname
        return ''

    def clone(self, **kwargs):
        upstream_copy = self.__class__(self.name, self.endpoints)
        upstream_copy.__dict__.update(**kwargs)
        upstream_copy.id = uuid.uuid1()
        return upstream_copy
