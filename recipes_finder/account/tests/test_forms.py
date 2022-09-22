from django.test import TestCase
from account.forms import UserRegistrationForm


class UserRegistrationFormTestCase(TestCase):
    def test_valid_clean_password2(self):
        data = {
            'username': 'test_a',
            'password': 'test_password',
            'password2': 'test_password'
        }
        form = UserRegistrationForm(data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_password2(), 'test_password')

    def test_invalid_clean_password2(self):
        data = {
            'username': 'test_a',
            'password': 'test_password',
            'password2': 'wrong_password'
        }
        form = UserRegistrationForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(str(form['password2'].errors.as_data(
        )), "[ValidationError(['Passwords are not the same.'])]")
