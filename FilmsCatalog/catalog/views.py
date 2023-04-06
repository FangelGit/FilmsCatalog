from rest_framework.response import Response
from django.db.models import ProtectedError, Prefetch
from rest_framework.viewsets import ModelViewSet

from catalog.models import Country, Director, Film, User
from catalog.permissions import ReadOnly, IsOwner, IsSuperUser
from catalog.serializers import CountrySerializer, DirectorSerializer, FilmSerializer, UserSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
    permission_classes = [IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DirectorViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsOwner]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    films = Film.objects.all().prefetch_related('director')

    def perform_destroy(self, instance, films=films):
        director_films = films.filter(director=instance)
        if director_films:
            raise ProtectedError('PROTECTED', director_films)
        else:
            instance.delete()


class CountryViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsOwner]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class FilmViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsSuperUser | ReadOnly]
    queryset = Film.objects.all().select_related('director').prefetch_related(
        Prefetch('countries', queryset=Country.objects.all().only('name')))
    serializer_class = FilmSerializer
