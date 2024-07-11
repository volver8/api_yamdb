from rest_framework.permissions import AllowAny

from .serializers import CategorySerializer
from .viewsets import ListCreateDestroyView
from reviews.models import Category


class CategoryViewSet(ListCreateDestroyView):
    """Вьюсет категорий."""
    permission_classes = (AllowAny, )
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
