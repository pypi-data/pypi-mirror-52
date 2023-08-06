# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
from ddd_base import ValueObject


class RouteSpecification(ValueObject):

    def __init__(self, api_ref, upstream_ref, policies, tls):
        super(RouteSpecification, self).__init__()
        self.api_ref = api_ref
        self.upstream_ref = upstream_ref
        self.policies = policies
        self.tls = tls

    @property
    def ssl(self):
        return True if self.tls == 'on' else False

    def __eq__(self, other):
        if not isinstance(other, RouteSpecification):
            return NotImplemented

        return self.api_ref == other.api_ref \
            and self.upstream_ref == other.upstream_ref \
            and self.policies == other.policies
