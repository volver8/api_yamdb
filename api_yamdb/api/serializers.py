from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Comment


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
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        """Представление объекта."""

        return TitleReadSerializer().to_representation(instance)


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на чтение."""

    category = CategorySerializer()
    genre = GenreSerializer(
        many=True,
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
            title = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                author=user,
                title=title
            ):
                raise serializers.ValidationError(
                    'Такой отзыв уже есть!'
                )
        if data['score'] > 10:
            raise serializers.ValidationError(
                'Оценка не может быть выше 10!'
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
