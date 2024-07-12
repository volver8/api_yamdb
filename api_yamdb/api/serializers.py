from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        genres = validated_data.pop('genres')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title

    # def create(self, validated_data):
    #     # Уберём список достижений из словаря validated_data и сохраним его
    #     achievements = validated_data.pop('achievements')

    #     # Создадим нового котика пока без достижений, данных нам достаточно
    #     cat = Cat.objects.create(**validated_data)

    #     # Для каждого достижения из списка достижений
    #     for achievement in achievements:
    #         # Создадим новую запись или получим существующий экземпляр из БД
    #         current_achievement, status = Achievement.objects.get_or_create(
    #             **achievement)
    #         # Поместим ссылку на каждое достижение во вспомогательную таблицу
    #         # Не забыв указать к какому котику оно относится
    #         GenreTitle.objects.create(
    #             achievement=current_achievement, cat=cat)
    #     return cat
