
from django.test import TestCase

from fpiweb.models import \
    Activity, \
    Box, \
    BoxType, \
    Product


class BoxTest(TestCase):

    fixtures = (
        'ProductCategory',
        'BoxType',
        'Product',
    )

    @staticmethod
    def test_add() -> None:

        box_number = 'BOX50001'
        # product = Product.objects.first()
        box = Box.objects.create(
            box_number=box_number,
            box_type=Box.box_type_default(),
            # exp_year=2022,
        )

        assert box.box_type is not None

        # call the method under test
        # box.add()

        activities = Activity.objects.filter(
            box_number=box_number
        )
        assert activities.count() == 0

        # activity = activities.first()
        box_type = BoxType.objects.get(box_type_code='Evans')
        # assert box_type.box_type_code == activity.box_type
        # assert activity.loc_row == ''
        # assert activity.loc_bin == ''
        # assert activity.loc_tier == ''


