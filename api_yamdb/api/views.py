from rest_framework import (
    filters,
    status,
    views,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from reviews.models import Category, Genre, Title, Review
from users.models import User
from .viewsets import CategoryGenreViewSet
from .filters import TitlesFilter
from .permissions import (
    IsAdminOrReadOnly,
    AuthorOrReadOnly,
    IsAdminOrSuper
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
    ReviewSerializer,
    CommentSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer
)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuper,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
    def update_profile(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class SignUpView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username'),
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Код: {confirmation_code}.',
            from_email=settings.EMAIL_ADMIN,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthTokenView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': ['Код подтверждения неверный']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = AccessToken.for_user(user)
        return Response({'token': str(access_token)})


class CategoryViewSet(CategoryGenreViewSet):
    """Вьюсет категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    """Вьюсет жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Обработка произведений."""

    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitlesFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    ordering_fields = ('name', 'year', 'rating')

    def get_serializer_class(self):
        """Выбор сериализатора."""

        if self.action in ('list', 'retrieve'):
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
    """Вьюсет отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
