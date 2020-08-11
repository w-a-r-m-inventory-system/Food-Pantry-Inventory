"""
PermissionsManagement.py - Manage user permissions
"""
from logging import getLogger
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from fpiweb.models import Profile
from fpiweb.constants import \
    UserInfo, \
    AccessLevel, \
    TargetUser, \
    InternalError, \
    AccessDict, \
    AccessGroupsAndFlags

logger = getLogger('fpiweb')


class ManageUserPermissions:
    """
    Manage user permissions
    """

    def __init__(self):
        self.vol_group = Group.objects.get(name=AccessLevel.Volunteer.name)
        self.staff_group = Group.objects.get(name=AccessLevel.Staff.name)
        self.admin_group = Group.objects.get(name=AccessLevel.Admin.name)

        return

    def get_user_info(self, user_id: int) -> UserInfo:
        """
        Return full user info for a given user.

        :param user_id: User record or user id
        :return: Full user info
        """
        user_rec = get_user_model().objects.get(pk=user_id)
        profile_rec = Profile.objects.get(user=user_rec)
        access_level = self.get_highest_access_level(user_rec)

        user_info = UserInfo(
            user=user_rec,
            profile=profile_rec,
            highest_access_level=access_level,
            is_active=user_rec.is_active,
            is_superuser=user_rec.is_superuser,
        )
        return user_info

    def get_highest_access_level(self, user)-> AccessLevel:
        """
        Determine the highest level of access this user currently has.

        :param user: an auth_user record
        :return: access level for this user
        """
        access_level = AccessLevel.No_Access
        if user:
            groups = user.groups.all()
            for group in groups:
                level_info = AccessDict.get(group.name, AccessLevel.No_Access)
                level = level_info.access_level
                if level > access_level:
                    access_level = level

        return access_level

    def add_a_user(self, target_user: TargetUser) -> User:
        """
        Add a new user account to the system.

        :param target_user:
        :return:
        """
        # Validate attempt to add a user
        test_username = target_user.username
        # test_userpswd = target_user.userpswd
        # test_confirm_pwd = target_user.confirm_pwd
        test_force_pswd_change = target_user.force_password
        test_first_name = target_user.first_name
        test_last_name = target_user.last_name
        test_email = target_user.email
        test_title = target_user.title
        test_access_level = target_user.access_level
        test_is_active = target_user.is_active
        # test_is_superuser = target_user.is_superuser

        # TODO Jun 23 2020 travis - Add full valiation for a new user
        # user.DoesNotExist
        # user.MultipeObjectsReturned
        # user.clean()
        # user.username_validator
        # user.normalize_username
        # user.is_authenticated
        # user.is_active
        # user.full_clean() Calls, clean_fields(), clean() and
        #   validate_unique
        # user.refresh_from_db()
        # user.validate_unique()
        # user.prepare_database_save()
        # user.save_base()
        # install python-zxcvbn for sane password validation

        user = self._add_user(target_user)
        return user

    def change_a_user(self, userid: int, target_user: TargetUser) -> User:
        """
        Change an attribute of a user account

        :param userid: key of existing user record
        :param target_user: all potential changes to the user and profile
        :return: modified user recors from db
        """
        # do any final validation here
        if not get_user_model().objects.filter(
                username=userid).exists:
            raise InternalError(
                f'Attempt to channge user {target_user.username}, '
                f'(key = {userid}) '
                f'but user is not in the list of valid users'
            )
        user = self._change_user(userid=userid, target_user=target_user)
        return user

    def _add_user(self, target_user: TargetUser) -> User:
        """
        Private method to actually add a user to the system.

        :param target_user:
        :return: a valid user record
        """
        # This method is currently hard-coded to expect three access
        # levels: Volunteer, Staff, and Administrator.  If more access
        # levels are added, this code must be altered to handle the
        # additional levels.

        # unpack access level
        access = AccessDict[target_user.access_level]

        with transaction.atomic():
            user = get_user_model().objects.create_user(
                username=target_user.username,
                email=target_user.email,
                # password=target_user.userpswd,
                first_name=target_user.first_name,
                last_name=target_user.last_name,
                is_active=target_user.is_active,
                is_staff=access.is_staff_flag,
                is_superuser=access.is_superuser_flag,
            )
            user.save()

            profile = Profile.objects.create(
                user_id=user.id,
                title=target_user.title
            )
            profile.save()

            # this person gets to be in the volunteer group but
            # can only be in the admin group if she is also in the staff group
            user.groups.add(self.vol_group)
            if access.is_staff_group:
                user.groups.add(self.staff_group)
                if access.is_admin_group:
                    user.groups.add(self.admin_group)

        user.refresh_from_db()
        profile.refresh_from_db()
        return user

    def _change_user(self, userid: int, target_user: TargetUser) -> User:
        """
        Apply changes to the user info in the db and log.

        :param userid: key to user record
        :param target_user: all potential changes to the user reccord
        :return: the revised user record from the database
        """
        # This method is currently hard-coded to expect three access
        # levels: Volunteer, Staff, and Administrator.  If more access
        # levels are added, this code must be altered to handle the
        # additional levels.

        with transaction.atomic():
            try:
                user = get_user_model().objects.select_related('profile').get(
                    id=userid
                )
                profile = user.profile
            except ObjectDoesNotExist as exc:
                raise InternalError(exc)

            # apply changes to user, if needed
            if target_user.username != user.username:
                self.log_change(
                    username=target_user.username,
                    field='Username',
                    old=user.username,
                    new=target_user.username,
                )
                user.username = target_user.username
            # TODO Jun 27 2020 travis - deal with passwork change and
            #  force password change
            if target_user.first_name != user.first_name:
                self.log_change(
                    username=user.username,
                    field='First Name',
                    old=user.first_name,
                    new=target_user.first_name,
                )
                user.username = target_user.username
            if target_user.last_name != user.last_name:
                self.log_change(
                    username=user.username,
                    field='Last Name',
                    old=user.last_name,
                    new=target_user.last_name,
                )
                user.last_name = target_user.last_name
            if target_user.email != user.email:
                self.log_change(
                    username=user.username,
                    field='email',
                    old=user.email,
                    new=target_user.email,
                )
                user.email = target_user.email
            if target_user.is_active != user.is_active:
                self.log_change(
                    username=user.username,
                    field='is_active',
                    old=str(user.is_active),
                    new=str(target_user.is_active),
                )
                user.is_active = target_user.is_active
            user.save()

            # apply changes to permissions, if needed
            target_perms: AccessGroupsAndFlags = AccessDict[
                target_user.access_level]
            if user.is_superuser:
                user_perms: AccessGroupsAndFlags = AccessDict[
                    AccessLevel.Admin]
            elif user.is_staff:
                user_perms: AccessGroupsAndFlags = AccessDict[
                    AccessLevel.Staff]
            else:
                user_perms: AccessGroupsAndFlags = AccessDict[
                    AccessLevel.Volunteer]
            if target_perms is not user_perms:
                self.log_change(
                    username=target_user.username,
                    field='Permissions',
                    old=user_perms.name,
                    new=target_perms.name,
                )

                # this person gets to be in the volunteer group but
                # can only be in the admin group if she is also in the staff
                # group
                user.groups.clear()
                user.groups.add(self.vol_group)
                if target_perms.is_staff_flag:
                    user.groups.add(self.staff_group)
                    if target_perms.is_superuser_flag:
                        user.groups.add(self.admin_group)

            # apply changes to profile, if needed
            if target_user.title != profile.title:
                self.log_change(
                    username=target_user.username,
                    field='Title',
                    old=profile.title,
                    new=target_user.title
                )
                profile.title = target_user.title
                profile.save()
        user.refresh_from_db()
        profile.refresh_from_db()
        return user

    def log_change(self, username: str, field: str, old: str, new:str):
        """
        write an entry to the log about the change made.

        :param username: the userid of the person being changed
        :param field: the descriptive name of the field being change
        :param old:
        :param new:
        :return:
        """
        logger.info(f'Changed {field} from -->{old}<-- to -->{new}<-- for'
                    f' {username}')
        return


# EOF
