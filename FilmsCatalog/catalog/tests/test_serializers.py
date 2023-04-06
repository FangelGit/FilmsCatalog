from django.test import TestCase

import catalog
from catalog.models import Director, Country, Film
from catalog.serializers import UserSerializer, DirectorSerializer, CountrySerializer, FilmSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = catalog.models.User.objects.create(username='user1')

    def test_ok(self):
        expected_data = {
            'username': 'user1',
            'first_name': '',
            'last_name': '',
            'user_type': 0
        }
        serialized_data = UserSerializer(self.user1).data
        self.assertEqual(expected_data, serialized_data)


class DirectorSerializerTestCase(TestCase):
    def setUp(self):
        self.director1 = Director.objects.create(first_name='David', last_name='Lynch')

    def test_ok(self):
        expected_data = {
            'first_name': 'David',
            'last_name': 'Lynch',
            'birth_date': None,
        }
        serialized_data = DirectorSerializer(self.director1).data
        self.assertEqual(expected_data, serialized_data)


class CountrySerializerTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Poland')

    def test_ok(self):
        expected_data = {
            'name': 'Poland',
        }
        serialized_data = CountrySerializer(self.country).data
        self.assertEqual(expected_data, serialized_data)


class FilmTestCase(TestCase):
    def setUp(self):
        self.director1 = Director.objects.create( first_name='David', last_name='Lynch')
        self.country1 = Country.objects.create(name='Poland')
        self.film = Film.objects.create(title='Film 1', description='Description 1', director=self.director1)
        self.film.countries.add(self.country1)

    def test_str(self):
        expected_data = {
            "title": "Film 1",
            "description": "Description 1",
            "countries": [
                {
                    "name": "Poland"
                },
            ],
            "director": {
                "first_name": "David",
                "last_name": "Lynch",
                'birth_date': None,
            }
        }
        serialized_data = FilmSerializer(self.film).data
        self.assertEqual(expected_data, serialized_data)
