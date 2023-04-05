from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.username}'


class Director(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    director = models.ForeignKey(Director, on_delete=models.PROTECT)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return f'{self.title} {self.director}'
