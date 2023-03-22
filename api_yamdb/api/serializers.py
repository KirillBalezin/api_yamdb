import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (
    Category, Genre, Title, Review, Comment, User,
    NAME_USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH
)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug'
                                            )
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         many=True,
                                         slug_field='slug'
                                         )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = fields
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Повторное написание отзывов запрещено.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if not re.match(r'[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                "Имя пользователя содержит запрещённые символы"
            )
        if value == "me":
            raise serializers.ValidationError(
                "Имя пользователя не может быть 'me'"
            )
        if len(value) > NAME_USERNAME_MAX_LENGTH:
            raise serializers.ValidationError(
                "username не может быть длиннее 150 символов"
            )
        return value

    def validate_email(self, value):
        if len(value) > EMAIL_MAX_LENGTH:
            raise serializers.ValidationError(
                "email не может быть длиннее 254 символов"
            )
        return value

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if not re.match(r'[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                "Имя пользователя содержит запрещённые символы"
            )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if not re.match(r'[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                "Имя пользователя содержит запрещённые символы"
            )
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Имя пользователя не может быть 'me'"
            )
        if len(value) > NAME_USERNAME_MAX_LENGTH:
            raise serializers.ValidationError(
                "username не может быть длиннее 150 символов"
            )
        return value

    def validate_email(self, value):
        if len(value) > EMAIL_MAX_LENGTH:
            raise serializers.ValidationError(
                "email не может быть длиннее 254 символов"
            )
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
