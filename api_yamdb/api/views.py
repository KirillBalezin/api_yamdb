from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Categories, Genres, Titles, Review
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          ReviewSerializer,
                          CommentSerializer)
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ...

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ...

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
