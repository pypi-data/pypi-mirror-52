# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
from collections import namedtuple
from ddd_base import ValueObject
from .block import Block
from .exception import LocationError

LocationRewrite = namedtuple('LocationRewrite', ['destination'])
LocationProxy = namedtuple('LocationProxy', ['host'])


class Location(ValueObject, Block):

    def __init__(self, name=None, internal=False):
        super().__init__()
        self.name = name
        self.internal = internal
        self.rewrite = None
        self.proxy = None

    def __eq__(self, other):
        if not isinstance(other, Location):
            return NotImplemented

        return self.internal == other.internal \
            and self.proxy == other.proxy \
            and self.rewrite == other.rewrite \
            and self.name == other.name

    def append(self, block):
        if isinstance(block, LocationProxy):
            self.proxy = block
        elif isinstance(block, LocationRewrite):
            self.rewrite = block
        else:
            raise LocationError()

    def dump_rewrite(self):
        return self.dump("location-rewrite.conf.jinja2", {
            "name": self.name,
            "variables": self.sets,
            "destination_name": self.rewrite.destination.name,
        })

    def dump_proxy(self):
        return self.dump("location-proxy.conf.jinja2", {
            "name": self.name,
            "variables": self.sets,
            "host": self.proxy.host,
        })

    def smart_dump(self):
        return self.dump_rewrite() if self.internal is False else self.dump_proxy()
