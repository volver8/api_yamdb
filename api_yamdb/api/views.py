from rest_framework import filters, viewsets

from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .viewsets import ListCreateDestroyView
from reviews.models import Category, Genre, Title


class CategoryViewSet(ListCreateDestroyView):
    """Вьюсет категорий."""

    permission_classes = (IsAdminOrReadOnly, )
    queryset = Category.objects.all()
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('slug', )
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyView):
    """Вьюсет жанров."""

    permission_classes = (IsAdminOrReadOnly, )
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('slug', )
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""

    permission_classes = (IsAdminOrReadOnly, )
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
