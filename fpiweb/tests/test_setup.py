"""
test_setup.py - Activities required before testing can begin.
"""
from fpiweb.tests.AddPermissionData import setup_groups_and_permissions

import pytest


def setup_module():
    """
    Setup activities required before a test can begin.

    :return:
    """
    setup_groups_and_permissions()

@pytest.fixture(scope="session")
def add_permission_data():
    """
    Define a fixtureto add the permission data.

    :return:
    """
    setup_groups_and_permissions()

# EOF
