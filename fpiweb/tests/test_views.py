
__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

from bs4 import BeautifulSoup
from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from fpiweb.models import \
    Box, \
    BoxNumber, \
    BoxType, \
    Location, \
    LocRow, \
    LocBin, \
    LocTier, \
    Product


def management_form_post_data(
        prefix,
        total_forms,
        initial_forms=0,
        min_num_forms=0,
        max_num_forms=100):
    post_data = {
        'TOTAL_FORMS': total_forms,
        'INITIAL_FORMS': initial_forms,
        'MIN_NUM_FORMS': min_num_forms,
        'MAX_NUM_FORMS': max_num_forms,
    }
    return {f'{prefix}-{k}': v for k, v in post_data.items()}


def formset_form_post_data(prefix, form_index, form_data):
    form_data_out = {}
    for key, value in form_data.items():
        key = f'{prefix}-{form_index}-{key}'
        form_data_out[key] = value
    return form_data_out


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


class BuildPalletViewTest(TestCase):

    fixtures = (
        'Location',
        'LocRow',
        'LocBin',
        'LocTier',
        'Product',
        'ProductCategory',
        'Box',
        'BoxType'
    )

    def test_post(self):
        user = User.objects.create_user(
            'aturing',
            'aturing@example.com',
            'abc123',
        )

        client = Client()
        client.force_login(user)

        # Pick a specific Location
        location = Location.objects.get(
            loc_row__loc_row='01',
            loc_bin__loc_bin='02',
            loc_tier__loc_tier='A1',
        )

        number_of_boxes = 3

        # Get 3 boxes that AREN'T in that Location
        boxes = Box.objects.exclude(location=location)[:number_of_boxes]

        # choose a product that isn't in any of the boxes
        product = Product.objects \
            .exclude(pk__in=[b.product.pk for b in boxes]) \
            .first()

        exp_year = date.today().year + 3

        formset_prefix = 'box_forms'
        post_data =  {
            'loc_row': location.loc_row.pk,
            'loc_bin': location.loc_bin.pk,
            'loc_tier': location.loc_tier.pk,
        }
        post_data.update(
            management_form_post_data(formset_prefix, number_of_boxes)
        )

        for i, box in enumerate(boxes):
            box_data = {
                'id': box.id,
                'box_number': box.box_number,
                'product': product.pk,
                'exp_year': exp_year,
            }

            # set exp month start and end
            if i == 0:
                box_data['exp_month_start'] = 3
                box_data['exp_month_end'] = 6

            box_data = formset_form_post_data('id_box_forms', i, box_data)
            post_data.update(box_data)

        # convert all the values to strings
        post_data = {k: str(v) for k, v in post_data.items()}

        response = client.post(
            reverse('fpiweb:build_pallet'),
            post_data,
        )
        self.assertEqual(200, response.status_code)

        for i, box in enumerate(boxes):
            box.refresh_from_db()

            self.assertEqual(product, box.product)
            self.assertEqual(location, box.location)
            self.assertEqual(exp_year, box.exp_year)

            if i == 0:
                self.assertEqual(3, box.exp_month_start)
                self.assertEqual(6, box.exp_month_end)




