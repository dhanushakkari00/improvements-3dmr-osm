from django.test import TestCase, Client
from django.contrib.auth.models import User
from mainapp.models import Model, LatestModel, Comment, Location, Category
from django.urls import reverse
from datetime import date
import json
import zipfile
import os
import tempfile
import shutil
from django.test.utils import override_settings


@override_settings(MODEL_DIR=tempfile.gettempdir())
class APITestCase(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.environ["MODEL_DIR"] = self.test_dir
        os.makedirs(os.path.join(self.test_dir, "1"), exist_ok=True)
        with zipfile.ZipFile(os.path.join(self.test_dir, "1", "1.zip"), "w") as zipf:
            zipf.writestr("dummy.obj", "fake obj content")

        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.location = Location.objects.create(latitude=12.34, longitude=56.78)
        self.category = Category.objects.create(name="Buildings")

        self.model = Model.objects.create(
            author=self.user,
            model_id=1,
            revision=1,
            title="Test Model",
            description="A test model",
            rendered_description="rendered test",
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

        self.comment = Comment.objects.create(
            author=self.user,
            model=self.model,
            comment="Nice model!",
            rendered_comment="Nice model!",
            is_hidden=False
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        self.override.disable()

    def test_get_info(self):
        response = self.client.get(reverse('get_info', args=[self.model.model_id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], "Test Model")
        self.assertEqual(data['author'], self.user.username)
        self.assertEqual(data['desc'], "A test model")
        self.assertEqual(data['lat'], 12.34)
        self.assertEqual(data['lon'], 56.78)
        self.assertIn("Buildings", data['categories'])

    def test_get_info_hidden_model(self):
        self.model.is_hidden = True
        self.model.save()
        response = self.client.get(reverse('get_info', args=[self.model.model_id]))
        self.assertEqual(response.status_code, 404)

    def test_lookup_category(self):
        response = self.client.get(reverse('lookup_category', args=["Buildings", 1]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn(self.model.model_id, data)

    def test_lookup_tag(self):
        self.model.tags = {"shape": "pyramidal"}
        self.model.save()
        response = self.client.get(reverse('lookup_tag', args=["shape=pyramidal", 1]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(self.model.model_id, data)

    def test_lookup_author(self):
        response = self.client.get(reverse('lookup_author', args=[self.user.username, 1]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(self.model.model_id, data)

    def test_search_title(self):
        response = self.client.get(reverse('search_title', args=["Test", 1]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(self.model.model_id, data)

    def test_search_range(self):
        response = self.client.get(reverse('lookup_range', args=[12.34, 56.78, 1000, 1]))  
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(self.model.model_id, data)

    def test_search_full(self):
        request_data = {
            "title": "Test",
            "lat": 12.34,
            "lon": 56.78,
            "range": 1000,
            "author": self.user.username
        }
        response = self.client.post(reverse('search_full'), data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(self.model.model_id, data)

    def test_get_filelist(self):
        response = self.client.get(reverse('get_list', args=[self.model.model_id]))  
        self.assertEqual(response.status_code, 200)
        self.assertIn("dummy.obj", response.content.decode())

    def test_get_file_not_found(self):
        response = self.client.get(reverse('get_file', args=[self.model.model_id, "nonexistent.obj"])) 
        self.assertEqual(response.status_code, 404)
