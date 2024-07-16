from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryGenreViewSet(ListCreateDestroyViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
