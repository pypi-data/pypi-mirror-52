# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
from ddd_base import Entity
from .block import Block
from .location import Location
from .exception.server_error import ServerError


class Server(Entity, Block):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.locations = []
        self.tls = True

    def disable_tls(self):
        self.tls = False

    def append(self, block):
        if isinstance(block, Location):
            self.locations.append(block)
        else:
            raise ServerError()

    def smart_dump(self):
        locations_dump = [a_location.add_tab(a_location.smart_dump()) for a_location in self.locations]

        return self.dump("server.conf.jinja2", {
            "name": self.name,
            "variables": self.sets,
            "locations": locations_dump,
            "tls": self.tls,
        })
