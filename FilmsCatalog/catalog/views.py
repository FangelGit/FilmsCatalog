from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from catalog.models import User, Country, Director, Film
from catalog.serializers import UserSerializer, CountrySerializer, DirectorSerializer, FilmSerializer


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all().select_related('director').prefetch_related('countries')
    serializer_class = FilmSerializer
