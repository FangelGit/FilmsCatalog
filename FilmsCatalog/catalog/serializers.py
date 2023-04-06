from catalog.models import DEFAULT_PASSWORD, User

from drf_writable_nested import UniqueFieldsMixin, WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer

from catalog.models import Film, Country, Director


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'user_type')

    def create(self, validated_data):
        raw_password = DEFAULT_PASSWORD
        for attr, value in validated_data.items():
            if attr == 'password':
                raw_password = value
        obj = User.objects.create(**validated_data)
        obj.set_password(raw_password)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class CountrySerializer(UniqueFieldsMixin, ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')

    def create(self, validated_data):
        country = validated_data
        obj, _ = Country.objects.get_or_create(name=country['name'])
        return obj


class DirectorSerializer(ModelSerializer):
    class Meta:
        model = Director
        fields = ('id', 'first_name', 'last_name', 'birth_date')

    def create(self, validated_data):
        obj, is_new = Director.objects.get_or_create(first_name=validated_data['first_name'],
                                                     last_name=validated_data['last_name'],
                                                     birth_date=validated_data['birth_date'])
        return obj


class FilmSerializer(WritableNestedModelSerializer):
    countries = CountrySerializer(many=True, )  # read_only=True)
    director = DirectorSerializer(many=False, )  # read_only=True)

    class Meta:
        model = Film
        fields = ('title', 'description', 'countries', 'director')

