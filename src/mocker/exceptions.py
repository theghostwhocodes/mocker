# coding: utf-8
"""Custom exceptions for Mocker"""


class JSONKeyMissingException(Exception):
    """Exception to raise when there is a missing required key in mock file"""

    def __init__(self, message, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.message = message
