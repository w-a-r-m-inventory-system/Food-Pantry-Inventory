"""
Global constants and exceptions for this project.

Constants that don't have an obvious home elsewhere are defined here.

Non-Django-based exceptions are defined here.
"""

###########
# Constants
###########

#############################
# Project specific exceptions
#############################

class ProjectError(Exception):
    """
    All exceptions unique to this project wil be based on this class.
    """
    pass

class InternalError(ProjectError):
    """
    The error is raised when there is some interal logic problem.
    """

# EOF
