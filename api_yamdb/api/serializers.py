from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User
from users.constants import EMAIL_LEHGTH, MAX_LENGTH
from users.validators import validate_username


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH,
        validators=[UnicodeUsernameValidator(), validate_username]
    )


class SignUpSerializer(UsernameSerializer):
    email = serializers.EmailField(
        max_length=EMAIL_LEHGTH
    )

    def validate(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        user_email = User.objects.filter(email=email).first()
        user_username = User.objects.filter(username=username).first()
        if user_email != user_username:
            error_msg = {}
            if user_username:
                error_msg['username'] = ('Пользователь с таким username'
                                         'уже существует.')
            if user_email:
                error_msg['email'] = ('Пользователь с таким email'
                                      'уже существует.')
            raise serializers.ValidationError(error_msg)
        return validated_data


class TokenSerializer(UsernameSerializer):
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категории."""

    class Meta:
        fields = ('name', 'slug', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанра."""

    class Meta:
        fields = ('name', 'slug', )
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на запись."""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_null=True,
        allow_empty=False,
    )

    class Meta:
        model = Title
        fields = ('name',
                  'year',
                  'description',
                  'genre',
                  'category')

    def to_representation(self, instance):
        """Представление объекта."""
        return (TitleReadSerializer(self, context=self.context)
                .to_representation(instance))


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на чтение."""

    category = CategorySerializer()
    genre = GenreSerializer(
        many=True,
        allow_null=True,
        allow_empty=True
    )
    rating = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['view'].action == 'create':
            user = self.context.get('request').user
            title = get_object_or_404(
                Title, pk=self.context.get('view').kwargs.get('title_id')
            )
            if Review.objects.filter(
                author=user,
                title=title
            ):
                raise serializers.ValidationError(
                    'Такой отзыв уже есть!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
