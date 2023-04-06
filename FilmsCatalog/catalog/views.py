from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from django.db.models import ProtectedError, Prefetch
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from catalog.models import Country, Director, Film, User, TYPE_CHOICES
from catalog.permissions import ReadOnly, IsOwner, IsSuperUser
from catalog.serializers import CountrySerializer, DirectorSerializer, FilmSerializer, UserSerializer, LoginSerializer, \
    UserTypeSerializer


# Create your views here.
def user_type_to_str(user_type):
    for choice in TYPE_CHOICES:
        if user_type == choice[0]:
            return choice[1]



class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        str_user_type = user_type_to_str(user.user_type)
        return Response(str_user_type, status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        if request.user.is_authenticated:
            # serializer = UserTypeSerializer(data=request.user, context={'request': request})
            # serializer.is_valid(raise_exception=True)
            # user_type = serializer.validated_data['type']
            str_user_type = user_type_to_str(request.user.user_type)
            response = Response(str_user_type, status=status.HTTP_200_OK)
        else:
            response = Response("Not logged in", status=status.HTTP_403_FORBIDDEN)
        return response

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
