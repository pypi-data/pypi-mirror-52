"""Custom Exceptions launched in clients"""
__author__ = 'eag'
__license__ = "see LICENSE file"


class ConfigurationError(Exception):
    pass


class AuthserverError(Exception):
    pass


class InvalidSignature(Exception):
    pass
