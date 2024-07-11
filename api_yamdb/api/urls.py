from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, GenreViewSet


router_v1 = SimpleRouter()

router_v1.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
