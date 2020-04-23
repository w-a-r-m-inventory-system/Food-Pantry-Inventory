"""
Global constants, constructs and exceptions for this project.

Constants and constructs that don't have an obvious home elsewhere are
defined here.

Non-Django-based exceptions are defined here.
"""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum, IntEnum
from typing import NamedTuple, List

from django.core.exceptions import ValidationError

# # # # # #
# Constants
# # # # # #

CURRENT_YEAR = date.today().year
""" The current year - used for validating expiration dates """

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class HTTP_STATUS(IntEnum):
    """
    Status response codes (subset used by this application)

    These status codes are defined in
    `RFC 7231 <https://tools.ietf.org/html/rfc7231.html>`_
    """
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    I_AM_A_TEAPOT = 418
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501

# # # # # # # # # # # # # # #
# Project specific exceptions
# # # # # # # # # # # # # # #

class ProjectError(ValidationError):
    """
    All exceptions unique to this project wil be based on this class.
    """
    pass


class InvalidValueError(ProjectError):
    """
    Used when an invalid value has been passed as a parameter.
    """
    pass


class InvalidActionAttemptedError(ProjectError):
    """
    A requested action cannot be done at this time.
    """
    pass


class InternalError(ProjectError):
    """
    The error is raised when there is some interal logic problem.
    """

@dataclass
class ValidOrErrorResponse():
    """
    A constructed response denoting either valid or has error messages.
    """
    is_valid: bool = True
    error_msg_list: List[str] = field(default_factory=list)

    def add_error(self, msg: str):
        """
        Set as invalid and add an error message.

        :param msg: error message to add
        :return:
        """
        self.is_valid = False
        self.error_msg_list.append(msg)
        return

    def __repr__(self):
        display = ''
        if self.is_valid:
            display = "Valid"
        else:
            display = f'Invalid: {self.error_msg_list[0]}'
            if len(self.error_msg_list) > 1:
                for msg in self.error_msg_list[1:]:
                    display += f', {msg}'
        return display

# EOF
