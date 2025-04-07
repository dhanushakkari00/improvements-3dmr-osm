from django.test import TestCase
from django.contrib.auth.models import User
from mainapp.models import Profile,Ban

class ProfileModelTest(TestCase):
    def setUp(self):
        #Set up test data before each test method is run
        self.user = User.objects.create(username = "testuser")
        self.admin_user = User.objects.create(username = "adminuser" , is_staff = True)
        self.profile = self.user.profile
    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        #As the default description is "Your description..." we will verify it
        self.assertEqual(self.profile.description, "Your description...")
        #Default rendered_description is ""<p>Your description...</p>""
        self.assertEqual(self.profile.rendered_description ,"<p>Your description...</p>")
    def test_banned_false(self):
        #Checking if is_banned is false when the user is not banned
        self.assertFalse(self.profile.is_banned)
    def test_banned_true(self):
        #Chceking if is_banned is true after banning the user
        Ban.objects.create(admin = self.admin_user , banned_user = self.user, reason = "Testing ban funcationality")
        self.assertTrue(self.profile.is_banned)
    def test_avatar(self):
        self.user.social_auth.create(provider ="osm" , uid = "12345",extra_data={"avatar":"http://example.com/avatar.jpg"})
        self.assertTrue(self.profile.avatar.startswith("https://"))