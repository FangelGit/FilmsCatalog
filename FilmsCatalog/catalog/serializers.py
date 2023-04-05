from rest_framework.serializers import ModelSerializer

from catalog.models import User, Film, Country, Director


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ('name',)


class DirectorSerializer(ModelSerializer):
    class Meta:
        model = Director
        fields = ('first_name', 'last_name')


class FilmSerializer(ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)
    director = DirectorSerializer(many=False, read_only=True)

    class Meta:
        model = Film
        fields = ('title', 'description', 'countries', 'director')
