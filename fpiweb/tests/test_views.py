
__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

from bs4 import BeautifulSoup

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from fpiweb.forms import \
    ExtantBoxNumberForm, \
    ExistingLocationForm
from fpiweb.models import \
    Box, \
    BoxNumber, \
    BoxType, \
    Location, \
    Product
from fpiweb.views import ManualMoveBoxView


class BoxNewViewTest(TestCase):

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

        box_number = BoxNumber.format_box_number(1)
        url = reverse('fpiweb:box_new', args=(box_number,))

        box_type = BoxType.objects.get(box_type_code='Evans')

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
        self.assertEqual(302, response.status_code, str(response.content))

        box = Box.objects.order_by('-pk').first()
        self.assertEqual(
            reverse('fpiweb:box_details', args=(box.pk,)),
            response.url
        )

        box = Box.objects.get(box_number=box_number)

        self.assertEqual(box_type, box.box_type)
        self.assertEqual(box_type.box_type_qty, box.quantity)


class IndexViewTest(TestCase):

    def test_get(self):
        client = Client()
        response = client.get(reverse('fpiweb:index'))
        self.assertEqual(200, response.status_code)


class AboutView(TestCase):

    def test_get(self):
        client = Client()
        response = client.get(reverse('fpiweb:about'))
        self.assertEqual(200, response.status_code)


class LoginView(TestCase):

    def test_get(self):
        client = Client()
        response = client.get(reverse('fpiweb:login'))
        self.assertEqual(200, response.status_code)

    def test_post(self):
        username = 'jdoe'
        password = 'abc123'
        User.objects.create_user(username, 'jdoe@example.com', password)

        client = Client()
        url = reverse('fpiweb:login')

        response = client.post(
            url,
            {
                'username': username,
                'password': password,
            },
        )

        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('fpiweb:index'), response.url)

        response = client.post(
            url,
            {
                'username': username,
                'password': 'NARF!!',
            },
        )

        # yeah, FormViews like this one return 200 status code if form
        # fails validation
        self.assertEqual(200, response.status_code)

        soup = BeautifulSoup(response.content, 'html.parser')
        error_list = soup.find('ul', class_='errorlist')
        self.assertIsNotNone(error_list)
        self.assertIn(
            "Invalid username and/or password",
            error_list.get_text(),
        )

    def test_login_required_redirects_to_login_view(self):
        client = Client()
        response = client.get(reverse('fpiweb:maintenance'))
        self.assertEqual(302, response.status_code)
        self.assertTrue(response.url.startswith(reverse('fpiweb:login')))


class LogoutViewTest(TestCase):

    def test_get(self):
        client = Client()
        response = client.get(reverse('fpiweb:logout'))
        self.assertEqual(200, response.status_code)


class ManualMoveBoxViewTest(TestCase):

    fixtures = (
        'BoxType',
        'ProductCategory',
        'Product',
        'LocRow',
        'LocBin',
        'LocTier',
        'Location',
    )

    url = reverse_lazy('fpiweb:manual_move_box')

    def test_get(self):
        user = User.objects.create_user('jdoe3', 'jdoe2@foo.com', 'abc123')

        client = Client()
        client.force_login(user)

        response = client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            ManualMoveBoxView.MODE_ENTER_BOX_NUMBER,
            response.context.get('mode'),
        )

        box_number_form = response.context.get('box_number_form')
        self.assertIsInstance(box_number_form, ExtantBoxNumberForm)
        self.assertIsNone(response.context['box'])
        self.assertIsNone(response.context['location_form'])
        self.assertIsNone(response.context['errors'])

    def test_post_box_number_form(self):
        user = User.objects.create_user('jdoe4', 'jdoe4@foo.com', 'abc123')

        client = Client()
        client.force_login(user)

        box_number = BoxNumber.get_next_box_number()

        response = client.post(
            self.url,
            {
                'mode': ManualMoveBoxView.MODE_ENTER_BOX_NUMBER,
                'box_number': box_number
            },
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(
            ManualMoveBoxView.MODE_ENTER_BOX_NUMBER,
            response.context['mode'],
        )
        self.assertIsInstance(
            response.context['box_number_form'],
            ExtantBoxNumberForm,
        )

        box = Box.objects.create(
            box_number=box_number,
            box_type=BoxType.objects.get(box_type_code='Evans'),
            product=Product.objects.get(prod_name='Canned Potatoes'),
        )

        response = client.post(
            self.url,
            {
                'mode': ManualMoveBoxView.MODE_ENTER_BOX_NUMBER,
                'box_number': box_number
            }
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            ManualMoveBoxView.MODE_ENTER_LOCATION,
            response.context['mode'],
        )
        self.assertEqual(
            response.context['box'].box_number,
            box.box_number
        )
        self.assertIsInstance(
            response.context['location_form'],
            ExistingLocationForm,
        )

    def test_post_location_form(self):
        user = User.objects.create_user('jdoe5', 'jdoe5@foo.com', 'abc123')

        client = Client()
        client.force_login(user)

        box = Box.objects.create(
            box_number=BoxNumber.get_next_box_number(),
            box_type=BoxType.objects.get(box_type_code='Evans'),
            product=Product.objects.get(prod_name='Canned Potatoes'),
            date_filled=timezone.now(),
            exp_year=2022,
        )
        self.assertIsNone(box.location)

        location = Location.objects.first()

        response = client.post(
            self.url,
            {
                'mode': ManualMoveBoxView.MODE_ENTER_LOCATION,
                'loc_row': location.loc_row_id,
                'loc_bin': location.loc_bin_id,
                'loc_tier': location.loc_tier_id,
                'box_pk': box.pk,
            }
        )

        self.assertEqual(200, response.status_code, response.content)

        context_box = response.context.get('box')
        self.assertIsNotNone(context_box)
        self.assertEqual(
            box.pk,
            context_box.pk,
        )
        self.assertEqual(
            location.pk,
            context_box.location.pk,
        )

