import datetime as dt

from rest_framework import serializers

from reviews.models import Categories, Genres, Titles


class GenresSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        read_only=True,
        slug_field='genre_slug'
    )

    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class CategoriesSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        read_only=True,
        slug_field='category_slug'
    )

    class Meta:
        fields = '__all__'
        model = Categories