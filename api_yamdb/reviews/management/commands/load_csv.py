from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


TABLES_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов'

    def handle(self, *args, **options):
        for model_name, file_name in TABLES_DICT.items():
            try:
                with open(
                    f'./static/data/{file_name}',
                    encoding='utf-8'
                ) as csv_file:
                    data_list = []
                    data = DictReader(csv_file)
                    for row_data in data:
                        if 'category' in row_data:
                            row_data['category'] = Category.objects.get(
                                id=int(row_data['category'])
                            )
                        elif 'author' in row_data:
                            row_data['author'] = User.objects.get(
                                id=int(row_data['author'])
                            )
                        data_list.append(model_name(**row_data))
                    model_name.objects.bulk_create(data_list)
            except Exception as error:
                self.stdout.write(self.style.ERROR(f'{error}'))
        self.stdout.write(self.style.SUCCESS('Загрузка данных завершена'))
