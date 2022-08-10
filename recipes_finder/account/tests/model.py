from account.models import Profile
from django.contrib.auth.models import User
from django.test import TestCase


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', password='12345')
        self.profile = Profile.objects.create(
            nickname='usernick', user=self.user)

    def test_model_str(self):
        self.assertEqual(
            str(self.profile), f'Profile for user {self.user.username}')

    def tearDown(self):
        self.user.delete()
        self.profile.delete()
