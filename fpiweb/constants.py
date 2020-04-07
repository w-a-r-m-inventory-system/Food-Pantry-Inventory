"""
Global constants and exceptions for this project.

Constants that don't have an obvious home elsewhere are defined here.

Non-Django-based exceptions are defined here.
"""

from datetime import date

# # # # # #
# Constants
# # # # # #

CURRENT_YEAR = date.today().year
""" The current year - used for validating expiration dates """


# # # # # # # # # # # # # # #
# Project specific exceptions
# # # # # # # # # # # # # # #

class ProjectError(Exception):
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

# EOF
