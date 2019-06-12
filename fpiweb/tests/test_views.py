
__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from fpiweb.models import Box, BoxType


class BoxAddViewTest(TestCase):

    # The second time I ran this test I got the following error:
    #
    # ...
    #       min_value, max_value = Constraints.get_values(constraint_name)
    # TypeError: cannot unpack non-iterable NoneType object
    #
    # [Translation: We don't have any Constraint records in the database, so
    # fixture time]
    #
    # Fixtures are files located in fpiweb/fixtures, you don't need to include
    # the .json part of the filename.  Note: if you have a tuple with only 1
    # item in it [ i.e. ('foo', ) ] the trailing comma is important.  With it
    # it's a 1 item tuple, without it's a expression with a redundant set of
    # parenthesis around it.  PyCharm will complain about the redundant
    # parenthesis.
    fixtures = ('Constraints', 'BoxType')

    def test_get_success_url(self):

        # create user for this test (It will only exist briefly in the test
        # database).
        user = User.objects.create_user(
            'awesterville',
            'alice.westerville@example.com',
            'abc123')

        # Client sends HTTP requests and receives HTTP responses like a user's
        # browser.  It doesn't run any JavaScript, for that you need to use
        # Selenium to control a real browser.
        client = Client()

        # The first time I ran this test, I found that response.url was the
        # login page.  Ooops, forgot to log in.  Call the force_login method
        # to make Django act like we've gone through the login page
        client.force_login(user)

        url = reverse('fpiweb:box_new')

        box_type = BoxType.objects.get(box_type_code='Evans')

        box_number = 'box0001'
        post_data = {
            'box_number': box_number,
            'box_type': box_type.pk,
        }

        response = client.post(url, post_data)

        # Check whether the HTTP status code is 200, if it's not display the
        # text of the page returned.  Sometimes this makes looking for what
        # happened like looking for a needle in a haystack.

        # Unit-testing frameworks like unittest or pytest may discard text
        # sent to the terminal (stdout) unless a test fails.
        # print(dir(response))

        # Here's a handy page to bookmark:
        #     https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        #
        # Status code 418 is my favorite!
        self.assertEqual(302, response.status_code, response.content)
        self.assertEqual(reverse('fpiweb:index'), response.url)

        box = Box.objects.get(box_number=box_number)

        self.assertEqual(box_type, box.box_type)
        self.assertEqual(box_type.box_type_qty, box.quantity)
        self.assertTrue(box.print_box_number_label)

