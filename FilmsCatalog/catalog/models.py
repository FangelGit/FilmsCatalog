from django.contrib.auth.models import AbstractUser
from django.db import models

DEFAULT_PASSWORD = 'JMu9f27rNV'


def validate_birth_date(value):
    from datetime import datetime
    from rest_framework.exceptions import ValidationError

    if value <= datetime.now().date():
        return value
    else:
        raise ValidationError("Date is not passed")


TYPE_CHOICES = (
    (0, 'user'),
    (1, 'superuser'),
    (2, 'owner'),
)


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    user_type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=0)

    def __str__(self):
        return f'{self.username}'


class Director(models.Model):
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    birth_date = models.DateField(null=True, validators=[validate_birth_date])

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    director = models.ForeignKey(Director, on_delete=models.PROTECT)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return f'{self.title} {self.director}'
