"""
Global constants, constructs and exceptions for this project.

Constants and constructs that don't have an obvious home elsewhere are
defined here.

Non-Django-based exceptions are defined here.
"""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum, IntEnum, auto
from typing import NamedTuple, List, Dict

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from fpiweb.models import Profile

# # # # # # # # # # # #
# Decorator Definitions
# # # # # # # # # # # #
# use the following as a decorator for enums so templates will handle enums
# properly
def EnumForDjango(cls):
    cls.do_not_call_in_templates = True
    return cls

# # # # # # # # # # # # # #
# Special subclass of Enum
# # # # # # # # # # # # # #


class OrderedEnum(Enum):
    """
    Enhanced Enum class that considers the members as ordered
    """

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


# # # # # #
# Constants
# # # # # #

CURRENT_YEAR = date.today().year
""" The current year - used for validating expiration dates """

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

MINIMUM_PASSWORD_LENGTH: int = 10

QR_LABELS_PER_PAGE = 12

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
class ValidOrErrorResponse:
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
        if self.is_valid:
            display = "Valid"
        else:
            display = f'Invalid: {self.error_msg_list[0]}'
            if len(self.error_msg_list) > 1:
                for msg in self.error_msg_list[1:]:
                    display += f', {msg}'
        return display

@EnumForDjango
class AccessLevel(OrderedEnum):
    """
    Level of access for a user - lowest to highest.
    """
    No_Access: int = 0
    Volunteer: int = 10
    Staff: int = 50
    Admin: int = 99

    def __str__(self) -> str:
        display = f'{self.name} ({self.value})'
        return display


# class AccessLevelName:
#     """
#     Names for strings representing the access levels.
#     """
#
#     PERM_VOLUNTEER = AccessLevel.Volunteer.name
#     PERM_STAFF = AccessLevel.Staff.name
#     PERM_ADMIN = AccessLevel.Admin.name

# AccessLevelDict = {text: level for text, level in
#                    AccessLevel.__members__.items()}


class AccessGroupsAndFlags:
    """
    Unpacked attributes of an access level.
    """
    access_level: AccessLevel = None
    name: str = None
    value: int = None
    is_volunteer_group: bool = None
    is_staff_group: bool = None
    is_admin_group: bool = None
    is_staff_flag: bool = None
    is_superuser_flag: bool = None

    def __init__(self, access_level: AccessLevel):
        if access_level == AccessLevel.Volunteer:
            self.access_level = AccessLevel['Volunteer']
            self.name = self.access_level.name
            self.value = self.access_level.value
            self.is_volunteer_group = True
            self.is_staff_group = False
            self.is_admin_group = False
            self.is_staff_flag = False
            self.is_superuser_flag = False
        elif access_level == AccessLevel.Staff:
            self.access_level = AccessLevel['Staff']
            self.name = self.access_level.name
            self.value = self.access_level.value
            self.is_volunteer_group = True
            self.is_staff_group = True
            self.is_admin_group = False
            self.is_staff_flag = True
            self.is_superuser_flag = False
        elif access_level == AccessLevel.Admin:
            self.access_level = AccessLevel['Admin']
            self.name = self.access_level.name
            self.value = self.access_level.value
            self.is_volunteer_group = True
            self.is_staff_group = True
            self.is_admin_group = True
            self.is_staff_flag = True
            self.is_superuser_flag = True
        else:
            self.access_level = AccessLevel['No_Access']
            self.name = self.access_level.name
            self.value = self.access_level.value
            self.is_volunteer_group = False
            self.is_staff_group = False
            self.is_admin_group = False
            self.is_staff_flag = False
            self.is_superuser_flag = False
        return

    def __str__(self) -> str:
        """
        Provide a printable representation of entry.

        :return: printable representation
        """
        display = f'Access level: {self.name} ({self.value}), Groups: ' \
                  f'Vol-{"Y" if self.is_volunteer_group else "N"}, ' \
                  f'Staff-{"Y" if self.is_staff_group else "N"}, ' \
                  f'Admin-{"Y" if self.is_admin_group else "N"} ' \
                  f'Flags: Staff-{"Y" if self.is_staff_flag else "N"}, ' \
                  f'Super-{"Y" if self.is_superuser_flag else "N"}'
        return display

def load_access_dict()-> Dict:
    """
    Load a multipurpose dictionary with all access level identifieres.

    :return: a dictionary with lots of keys
    """
    ad = dict()
    for access_level in AccessLevel:
        access_group_flags = AccessGroupsAndFlags(access_level=access_level)
        ad[access_level] = access_group_flags
        ad[access_level.name] = access_group_flags
        ad[access_level.value] = access_group_flags
        ad[str(access_level)] = access_group_flags
    return ad

AccessDict = load_access_dict()


# @dataclass
class AccessGroupsAndFlags:
    """
    Unpacked attributes of an access level.
    """
    access_level: AccessLevel = None
    name: str = None
    value: int = None
    is_volunteer_group: bool = None
    is_staff_group: bool = None
    is_admin_group: bool = None
    is_staff_flag: bool = None
    is_superuser_flag: bool = None

    def __init__(self, access_level: AccessLevel):
        if access_level == AccessLevel.Volunteer:
            self.access_level = AccessLevel.Volunteer
            self.name = self.access_level.name
            self.value = self.access_level.value
            self.is_volunteer_group = True
            self.is_staff_group = False
            self.is_admin_group = False
            self.is_staff_flag = False
            self.is_superuser_flag = False
        elif access_level == AccessLevel.Staff:
            self.access_level = AccessLevel.Staff
            self.name = self.access_level.name
            self.value = self.access_level.value
            self.is_volunteer_group = True
            self.is_staff_group = True
            self.is_admin_group = False
            self.is_staff_flag = True
            self.is_superuser_flag = False
        elif access_level == AccessLevel.Admin:
            self.access_level = AccessLevel.Admin
            self.name = self.access_level.name
            self.value = self.access_level.value
            self.is_volunteer_group = True
            self.is_staff_group = True
            self.is_admin_group = True
            self.is_staff_flag = True
            self.is_superuser_flag = True
        else:
            self.access_level = AccessLevel.No_Access
            self.name = self.access_level.name
            self.value = self.access_level.value
            self.is_volunteer_group = False
            self.is_staff_group = False
            self.is_admin_group = False
            self.is_staff_flag = False
            self.is_superuser_flag = False
        return

    def __str__(self) -> str:
        """
        Provide a printable representation of entry.

        :return: printable representation
        """
        display = f'Access level: {self.name} ({self.value}), Groups: ' \
                  f'Vol-{"Y" if self.is_volunteer_group else "N"}, ' \
                  f'Staff-{"Y" if self.is_staff_group else "N"}, ' \
                  f'Admin-{"Y" if self.is_admin_group else "N"} ' \
                  f'Flags: Staff-{"Y" if self.is_staff_flag else "N"}, ' \
                  f'Super-{"Y" if self.is_superuser_flag else "N"}'
        return display

def load_access_dict()-> Dict:
    """
    Load a multipurpose dictionary with all access level identifieres.

    :return: a dictionary with lots of keys
    """
    ad = dict()
    for access_level in AccessLevel:
        access_group_flags = AccessGroupsAndFlags(access_level=access_level)
        ad[access_level] = access_group_flags
        ad[access_level.name] = access_group_flags
        ad[access_level.value] = access_group_flags
        ad[str(access_level)] = access_group_flags
    return ad

AccessDict = load_access_dict()


class UserInfo(NamedTuple):
    """
    Information about a specific user - abstracted from various tables.
    """

    user: User
    profile: Profile
    highest_access_level: AccessLevel
    is_active: bool
    is_superuser: bool

    def get_sort_key(self) -> str:
        """
        Return a usable sort key
        :return:
        """
        fullname = self.user.get_full_name()
        level = f'{self.highest_access_level.value:03}'
        key = f'{level} {fullname}'
        return key

class TargetUser(NamedTuple):
    """
    User information to be added or updated.
    """
    username: str = ''
    # userpswd: str = ''
    # confirm_pwd: str = ''
    pswd_changed: bool = False
    force_password: bool = False
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    title: str = ''
    access_level: AccessLevel = AccessLevel.No_Access
    is_active: bool = True
    # is_staff: bool = False
    # is_superuser: bool = False

# EOF
