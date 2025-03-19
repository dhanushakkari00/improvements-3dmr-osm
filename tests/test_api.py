from django.test import TestCase, Client
from django.contrib.auth.models import User
from mainapp.models import Model, LatestModel, Comment, Location, Category
from django.urls import reverse
from datetime import date
import json

class APITestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create(username="testuser")

        self.location = Location.objects.create(latitude=12.34, longitude=56.78)

        self.category = Category.objects.create(name="Buildings")

        self.model = Model.objects.create(
            author=self.user,
            model_id=1,
            revision=1,
            title="Test Model",
            description="A test model",
            location=self.location,
            license=1,
            upload_date=date.today(),
            scale=1.0,
            rotation=0.0,
            translation_x=0.0,
            translation_y=0.0,
            translation_z=0.0,
            is_hidden=False
        )
        self.model.categories.add(self.category)

        # Create a comment
        self.comment = Comment.objects.create(
            author=self.user,
            model=self.model,
            comment="Nice model!",
            rendered_comment="Nice model!",
            is_hidden=False
        )

    def test_get_info(self):
        """Test GET /api/get_info/"""
        response = self.client.get(reverse('get_info', args=[self.model.model_id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], "Test Model")
        self.assertEqual(data['author'], self.user.username)

    def test_get_info_hidden_model(self):
        """Test GET /api/get_info/ for a hidden model"""
        self.model.is_hidden = True
        self.model.save()
        response = self.client.get(reverse('get_info', args=[self.model.model_id]))
        self.assertEqual(response.status_code, 404)

    def test_lookup_category(self):
        """Test GET /api/lookup_category/"""
        response = self.client.get(reverse('lookup_category', args=["Buildings", 1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_lookup_tag(self):
        """Test GET /api/lookup_tag/"""
        response = self.client.get(reverse('lookup_tag', args=["shape=pyramidal", 1]))
        self.assertEqual(response.status_code, 200)

    def test_lookup_author(self):
        """Test GET /api/lookup_author/"""
        response = self.client.get(reverse('lookup_author', args=[self.user.username, 1]))
        self.assertEqual(response.status_code, 200)

    def test_search_title(self):
        """Test GET /api/search_title/"""
        response = self.client.get(reverse('search_title', args=["Test", 1]))
        self.assertEqual(response.status_code, 200)

    def test_search_range(self):
        """Test GET /api/search_range/"""
        response = self.client.get(reverse('lookup_range', args=[12.34, 56.78, 1000, 1]))  
        self.assertEqual(response.status_code, 200)

    def test_search_full(self):
        """Test POST /api/search_full/"""
        request_data = {
            "title": "Test",
            "lat": 12.34,
            "lon": 56.78,
            "range": 1000,
            "author": self.user.username
        }
        response = self.client.post(reverse('search_full'), data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_filelist(self):
        """Test GET /api/get_filelist/"""
        response = self.client.get(reverse('get_filelist', args=[self.model.model_id]))  
        self.assertEqual(response.status_code, 200)

    def test_get_file_not_found(self):
        """Test GET /api/get_file/ with a non-existing file"""
        response = self.client.get(reverse('get_file', args=[self.model.model_id, "nonexistent.obj"])) 
        self.assertEqual(response.status_code, 404)
