from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import AuthTokenView, SignUpView, UserViewSet
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet,
                    CommentViewSet)


router_v1 = SimpleRouter()

router_v1.register(
    r'users',
    UserViewSet,
    basename='users'
)
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
router_v1.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', AuthTokenView.as_view(), name='auth_token'),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
]
