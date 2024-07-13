from rest_framework import serializers
from reviews.models import Genre, Category, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на запись."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        """Представление объекта."""
        view = self.context.get('view')
        if not view:
            raise serializers.ValidationError('Нет view.')
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
