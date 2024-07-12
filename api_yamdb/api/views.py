from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .viewsets import ListCreateDestroyView
from reviews.models import Category, Genre, Title


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
    """Вьюсет произведений."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, )
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
