# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
from .nginx_base_exception import NginxBaseException


class LocationError(NginxBaseException):

    """Generic exception for Nginx root"""
    def __init__(self, msg="Location error", original_exception=None):
        super(LocationError, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
