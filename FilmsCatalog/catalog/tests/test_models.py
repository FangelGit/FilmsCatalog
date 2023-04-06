from django.test import TestCase
import catalog
from catalog.models import Director, Country, Film


class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = catalog.models.User.objects.create(username='user1')

    def test_str(self):
        self.assertEqual('user1', str(self.user1))


class DirectorTestCase(TestCase):
    def setUp(self):

        self.director1 = Director.objects.create(first_name='David', last_name='Lynch')

    def test_str(self):
        self.assertEqual('David Lynch', str(self.director1))


class CountryTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Poland')

    def test_str(self):
        self.assertEqual('Poland', str(self.country))


class FilmTestCase(TestCase):
    def setUp(self):
        self.user1 = catalog.models.User.objects.create(username='user1')
        self.director1 = Director.objects.create(first_name='David', last_name='Lynch')
        self.country1 = Country.objects.create(name='Poland')
        self.film = Film.objects.create(title='Film 1', description='Description 1', director=self.director1)
        self.film.countries.add(self.country1)

    def test_str(self):
        self.assertEqual('Film 1 David Lynch', str(self.film))
