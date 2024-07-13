from rest_framework import filters, status, viewsets
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import GenericViewSet

from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleWriteSerializer,
                          TitleReadSerializer)
from reviews.models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .filters import TitlesFilter
from .viewsets import ListCreateDestroyView


class CategoryViewSet(ListCreateDestroyView):
    """Вьюсет категорий."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, )
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

    permission_classes = (IsAdminOrReadOnly,IsAuthenticatedOrReadOnly,)
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