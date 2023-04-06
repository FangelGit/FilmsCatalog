import json

from django.core import serializers
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

import catalog
from catalog.models import User, Director, Country, Film
from catalog.serializers import CountrySerializer, DirectorSerializer, UserSerializer, FilmSerializer


class CountryApiTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create(username='superuser', user_type=1)
        self.owner = User.objects.create(username='owner', user_type=2)
        self.user1 = User.objects.create(username='user1')

        self.director1 = Director.objects.create(first_name='David', last_name='Lynch')
        self.country1 = Country.objects.create(name='Poland')
        self.film = Film.objects.create(title='Film 1', description='Description 1', director=self.director1)
        self.film.countries.add(self.country1)
        self.countries = Country.objects.all()

    def test_get(self):
        url = reverse('country-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_superuser(self):
        url = reverse('country-list')
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_owner(self):
        url = reverse('country-list')
        expected_data = CountrySerializer(self.countries, many=True).data
        self.client.force_login(self.owner)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_post(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        url = reverse('country-list')
        self.assertEqual(1, Country.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Country.objects.all().count())

    def test_post_superuser(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        url = reverse('country-list')
        self.client.force_login(self.superuser)
        self.assertEqual(1, Country.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Country.objects.all().count())

    def test_post_owner(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.owner)
        url = reverse('country-list')
        self.assertEqual(1, Country.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Country.objects.all().count())

    def test_put(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        url = reverse('country-detail', args=(self.countries[0].id,))
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_superuser(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        url = reverse('country-detail', args=(self.countries[0].id,))
        self.client.force_login(self.superuser)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_owner(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        url = reverse('country-detail', args=(self.countries[0].id,))
        self.client.force_login(self.owner)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        self.assertEqual(data, response.data)

    def test_delete(self):
        self.assertEqual(1, Country.objects.all().count())
        url = reverse('country-detail', args=(self.countries[0].id,))
        response = self.client.delete(url, data=self.countries[0].id, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Country.objects.all().count())

    def test_delete_superuser(self):
        self.assertEqual(1, Country.objects.all().count())
        self.client.force_login(self.superuser)
        url = reverse('country-detail', args=(self.countries[0].id,))
        response = self.client.delete(url, data=self.countries[0].id, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Country.objects.all().count())

    def test_delete_owner(self):
        self.assertEqual(1, Country.objects.all().count())
        url = reverse('country-detail', args=(self.countries[0].id,))
        self.client.force_login(self.owner)
        response = self.client.delete(url, data=self.countries[0].id, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Country.objects.all().count())


class DirectorApiTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create(username='superuser', user_type=1)
        self.owner = User.objects.create(username='owner', user_type=2)
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        self.director1 = Director.objects.create(first_name='David', last_name='Lynch')
        self.country1 = Country.objects.create(name='Poland')
        self.film = Film.objects.create(title='Film 1', description='Description 1', director=self.director1)
        self.film.countries.add(self.country1)
        self.directors = Director.objects.all()

    def test_get(self):
        url = reverse('director-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_superuser(self):
        expected_data = DirectorSerializer(self.directors, many=True).data
        self.client.force_login(self.superuser)
        url = reverse('director-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_get_owner(self):
        expected_data = DirectorSerializer(self.directors, many=True).data
        self.client.force_login(self.owner)
        url = reverse('director-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_post(self):
        data = {
            'first_name': 'director',
            'last_name': '1'
        }
        json_data = json.dumps(data)
        url = reverse('director-list')
        self.assertEqual(1, self.directors.count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, self.directors.all().count())

    def test_post_superuser(self):
        data = {
            'first_name': 'director',
            'last_name': '1'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.superuser)
        url = reverse('director-list')
        self.assertEqual(1, Director.objects.all().count())

        response = self.client.post(url, data=json_data, content_type='application/json')
        print(data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Director.objects.all().count())

    def test_post_owner(self):
        data = {
            'first_name': 'director',
            'last_name': '1'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.owner)
        url = reverse('director-list')
        self.assertEqual(1, Director.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Director.objects.all().count())

    def test_put(self):
        data = {
            'first_name': 'director',
            'last_name': '1'
        }
        json_data = json.dumps(data)
        url = reverse('director-detail', args=(self.directors[0].id,))
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_superuser(self):
        data = {
            'first_name': 'director',
            'last_name': '1',
            'birth_date': None,
        }
        json_data = json.dumps(data)
        url = reverse('director-detail', args=(self.directors[0].id,))
        self.client.force_login(self.superuser)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        self.assertEqual(data, response.data)

    def test_put_owner(self):
        data = {
            'first_name': 'director',
            'last_name': '1',
            'birth_date': None,
        }
        json_data = json.dumps(data)
        url = reverse('director-detail', args=(self.directors[0].id,))
        self.client.force_login(self.owner)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        self.assertEqual(data, response.data)

    def test_delete(self):
        self.assertEqual(1, Director.objects.all().count())
        url = reverse('director-detail', args=(self.directors[0].id,))
        response = self.client.delete(url, data=self.directors[0].id, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Director.objects.all().count())

    def test_delete_superuser(self):
        self.assertEqual(1, Director.objects.all().count())
        url = reverse('director-detail', args=(self.directors[0].id,))
        self.client.force_login(self.superuser)
        with self.assertRaises(ProtectedError):
            self.client.delete(url, data=self.directors[0].id, content_type='application/json')

    def test_delete_owner(self):
        self.assertEqual(1, Director.objects.all().count())
        url = reverse('director-detail', args=(self.directors[0].id,))
        self.client.force_login(self.owner)
        with self.assertRaises(ProtectedError):
            self.client.delete(url, data=self.directors[0].id, content_type='application/json')


class UserApiTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create(username='superuser', user_type=1)
        self.user1 = User.objects.create(username='user1', user_type=0)
        self.user2 = User.objects.create(username='user2', user_type=0)
        self.user3 = User.objects.create(username='user3', user_type=0)
        self.owner = User.objects.create(username='owner', user_type=2)

        self.director1 = Director.objects.create(first_name='David', last_name='Lynch')
        self.country1 = Country.objects.create(name='Poland')
        self.film = Film.objects.create(title='Film 1', description='Description 1', director=self.director1)
        self.film.countries.add(self.country1)
        self.users = User.objects.all()

    def test_get(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_superuser(self):
        self.client.force_login(self.superuser)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_owner(self):
        expected_data = UserSerializer(self.users, many=True).data
        self.client.force_login(self.owner)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_post(self):
        data = {
            'username': 'quest',
            'user_type': 0,
        }
        json_data = json.dumps(data)
        url = reverse('user-list')
        self.assertEqual(5, self.users.count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(5, self.users.all().count())

    def test_post_superuser(self):
        data = {
            'username': 'quest',
            'user_type': 0,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.superuser)
        url = reverse('user-list')
        self.assertEqual(5, User.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(5, self.users.all().count())

    def test_post_owner(self):
        data = {
            'username': 'quest',
            'user_type': 0,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.owner)
        url = reverse('user-list')
        self.assertEqual(5, User.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(6, User.objects.all().count())

    def test_put(self):
        data = {
            'username': 'quest',
            'user_type': 0,
        }
        json_data = json.dumps(data)
        url = reverse('user-detail', args=(self.users[0].id,))
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_superuser(self):
        data = {
            'username': 'quest',
            'user_type': 0,
        }
        json_data = json.dumps(data)
        url = reverse('user-detail', args=(self.users[0].id,))
        self.client.force_login(self.superuser)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_owner(self):
        data = {
            'username': 'quest',
            'first_name': '',
            'last_name': '',
            'user_type': 0,
        }
        json_data = json.dumps(data)
        url = reverse('user-detail', args=(self.users[0].id,))
        self.client.force_login(self.owner)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        self.assertEqual(data, response.data)

    def test_delete(self):
        self.assertEqual(5, User.objects.all().count())
        url = reverse('user-detail', args=(self.users[0].id,))
        response = self.client.delete(url, data=self.users[0].id, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(5, User.objects.all().count())

    def test_delete_superuser(self):
        self.assertEqual(5, User.objects.all().count())
        url = reverse('user-detail', args=(self.users[0].id,))
        self.client.force_login(self.superuser)
        response = self.client.delete(url, data=self.users[0].id, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(5, User.objects.all().count())

    def test_delete_owner(self):
        self.assertEqual(5, User.objects.all().count())
        url = reverse('user-detail', args=(self.users[0].id,))
        self.client.force_login(self.owner)
        response = self.client.delete(url, data=self.users[0].id, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(4, User.objects.all().count())


class FilmApiTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create(username='superuser', user_type=1)
        self.owner = User.objects.create(username='owner', user_type=2)
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        self.director1 = Director.objects.create(first_name='David', last_name='Lynch')
        self.country1 = Country.objects.create(name='Poland')
        self.film = Film.objects.create(title='Film 1', description='Description 1', director=self.director1)
        self.film.countries.add(self.country1)
        self.films = Film.objects.all()
        self.countries = Country.objects.all()
        self.directors = Director.objects.all()

    def test_get(self):
        expected_data = FilmSerializer(self.films, many=True).data
        url = reverse('film-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_get_superuser(self):
        self.client.force_login(self.superuser)
        expected_data = FilmSerializer(self.films, many=True).data
        url = reverse('film-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_get_owner(self):
        self.client.force_login(self.owner)
        expected_data = FilmSerializer(self.films, many=True).data
        url = reverse('film-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_post(self):
        data = {
            'title': 'director',
            'description': '1',
            'countries': [
                {'name': 'Country1'},
                {'name': 'Country2'},
            ],
            'director': {
                'first_name': 'First',
                'last_name': 'Second',
            }
        }
        json_data = json.dumps(data)
        url = reverse('film-list')
        self.assertEqual(1, self.films.count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, self.films.count())

    def test_post_superuser(self):
        data = {
            'title': 'director',
            'description': '1',
            'countries': [
                {'name': 'Country1'},
                {'name': 'Country2'},
            ],
            'director': {
                'first_name': 'First',
                'last_name': 'Second',
            }
        }
        json_data = json.dumps(data)
        self.client.force_login(self.superuser)
        url = reverse('film-list')
        self.assertEqual(1, Film.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Film.objects.all().count())

    def test_post_owner(self):
        data = {
            'title': 'director',
            'description': '1',
            'countries': [
                {'name': 'Country1'},
                {'name': 'Country2'},
            ],
            'director': {
                'first_name': 'First',
                'last_name': 'Second',
            }
        }
        json_data = json.dumps(data)
        self.client.force_login(self.owner)
        url = reverse('film-list')
        self.assertEqual(1, Film.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Film.objects.all().count())

    def test_put(self):
        data = {
            'countries': [
                {'name': 'Country1'},
                {'name': 'Country2'},
            ],
        }
        json_data = json.dumps(data)
        url = reverse('film-detail', args=(self.films[0].id,))
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    # def test_put_superuser(self):
    #     data = {
    #         'title': 'New film',
    #         'description': '1',
    #         'countries': [
    #             {'name': 'Country1'},
    #             {'name': 'Country2'},
    #         ],
    #         'director': {
    #             'first_name': 'First',
    #             'last_name': 'Second',
    #         }
    #     }
    #     json_data = json.dumps(data)
    #     url = reverse('film-detail', args=(self.films[0].id,))
    #     self.client.force_login(self.superuser)
    #     response = self.client.put(url, data=json_data, content_type='application/json')
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     response = self.client.get(url)
    #     print(f'Expected: {data}\nResponsed: {response.data}')
    #     self.assertEqual(data, response.data)

    # def test_patch_superuser(self):
    #     data = {
    #         'title': 'New film',
    #         'description': '1',
    #         'director': {
    #             'first_name': 'First',
    #             'last_name': 'Second',
    #         }
    #     }
    #     json_data = json.dumps(data)
    #     url = reverse('film-detail', args=(self.films[0].id,))
    #     self.client.force_login(self.superuser)
    #     response = self.client.patch(url, data=json_data, content_type='application/json')
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     response = self.client.get(url)
    #     print(f'Expected: {data}\nResponsed: {response.data}')
    #     self.assertEqual(data, response.data)

    # def test_put_owner(self):
    #     data = {
    #         'first_name': 'director',
    #         'last_name': '1',
    #         'birth_date': None,
    #     }
    #     json_data = json.dumps(data)
    #     url = reverse('director-detail', args=(self.directors[0].id,))
    #     self.client.force_login(self.owner)
    #     response = self.client.put(url, data=json_data, content_type='application/json')
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     response = self.client.get(url)
    #     self.assertEqual(data, response.data)
    #
    # def test_delete(self):
    #     self.assertEqual(1, Director.objects.all().count())
    #     url = reverse('director-detail', args=(self.directors[0].id,))
    #     response = self.client.delete(url, data=self.directors[0].id, content_type='application/json')
    #     self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
    #     self.assertEqual(1, Director.objects.all().count())
    #
    # def test_delete_superuser(self):
    #     self.assertEqual(1, Director.objects.all().count())
    #     url = reverse('director-detail', args=(self.directors[0].id,))
    #     self.client.force_login(self.superuser)
    #     with self.assertRaises(ProtectedError):
    #         self.client.delete(url, data=self.directors[0].id, content_type='application/json')
    #
    # def test_delete_owner(self):
    #     self.assertEqual(1, Director.objects.all().count())
    #     url = reverse('director-detail', args=(self.directors[0].id,))
    #     self.client.force_login(self.owner)
    #     with self.assertRaises(ProtectedError):
    #         self.client.delete(url, data=self.directors[0].id, content_type='application/json')
