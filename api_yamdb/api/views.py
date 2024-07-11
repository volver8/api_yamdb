from rest_framework.permissions import AllowAny

from .serializers import CategorySerializer, GenreSerializer
from .viewsets import ListCreateDestroyView
from reviews.models import Category, Genre


class CategoryViewSet(ListCreateDestroyView):
    """Вьюсет категорий."""
    permission_classes = (AllowAny, )
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyView):
    """Вьюсет жанров."""
    permission_classes = (AllowAny, )
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
