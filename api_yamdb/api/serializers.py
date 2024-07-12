from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Title


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


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер произведений."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title

    def create(self, validated_data):
        genres_data = validated_data.pop('genre')
        category = validated_data.pop('category')
        category = Category.objects.get_or_create(**category)
        validated_data['category'] = category
        title = Title.objects.create(**validated_data)

        for genre in genres_data:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)

        return title
