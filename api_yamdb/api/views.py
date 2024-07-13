from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
    ReviewSerializer
)
from .viewsets import ListCreateDestroyView
from .filters import TitlesFilter
from reviews.models import Category, Genre, Title


class CategoryViewSet(ListCreateDestroyView):
    """Вьюсет категорий."""

    permission_classes = (IsAdminOrReadOnly, )
    queryset = Category.objects.all()
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyView):
    """Вьюсет жанров."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, )
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Обработка произведений."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitlesFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    ordering_fields = ('name', 'year', 'rating')

    def get_serializer_class(self):
        """Выбор сериализатора."""

        if self.action in {'list', 'retrieve'}:
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):

        """Набор произведений."""
        if self.action in {'list', 'retrieve'}:
            return Title.objects.annotate(
                rating=Avg('reviews__score')
            )
        return Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
