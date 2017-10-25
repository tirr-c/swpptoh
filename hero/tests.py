from django.test import TestCase, Client
from .models import Hero
import json

# Create your tests here.
class HeroTestCase(TestCase):
    def setUp(self):
        Hero.objects.create(name='Superman')
        Hero.objects.create(name='Batman')
        Hero.objects.create(name='Joker')

        self.client = Client()

    def test_hero_str(self):
        batman = Hero.objects.get(name='Batman')
        self.assertEqual(str(batman), 'Batman')

    def test_hero_detail_get(self):
        response = self.client.get('/api/hero/1')

        data = json.loads(response.content.decode())
        self.assertEqual(data['name'], 'Superman')
        self.assertEqual(response.status_code, 200)
