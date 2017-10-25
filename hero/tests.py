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

    def test_hero_detail_get_not_found(self):
        response = self.client.get('/api/hero/42')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_put(self):
        response = self.client.put('/api/hero/1', json.dumps({'name': 'foo'}), 'application/json')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/hero/1')
        data = json.loads(response.content.decode())
        self.assertEqual(data['name'], 'foo')
        self.assertEqual(response.status_code, 200)

    def test_hero_detail_put_not_found(self):
        response = self.client.put('/api/hero/42', json.dumps({'name': 'foo'}), 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_delete(self):
        response = self.client.delete('/api/hero/1')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/hero/1')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_delete_not_found(self):
        response = self.client.delete('/api/hero/42')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_method_not_allowed(self):
        response = self.client.post('/api/hero/1', json.dumps({'name': 'foo'}), 'application/json')
        self.assertEqual(response.status_code, 405)
