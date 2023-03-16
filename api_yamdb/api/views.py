from django.db.models import Avg

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Categories, Genres, Titles
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer)
from .permissions import AdminOrReadOnly

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().aggregate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year')
    ordering_fields = ('name', 'year')


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (
        AdminOrReadOnly,
    )


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (
        AdminOrReadOnly,
    )
