import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework.utils.model_meta import get_field_info

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = (f'Загружает данные в БД из csv.'
            f'csv файлы должны находиться в дериктории: '
            f'{settings.STATICFILES_DIRS[0]}')
    CATEGORY = 'static/data/category.csv'
    GENRE = 'static/data/genre.csv'
    USER = 'static/data/users.csv'
    TITLE = 'static/data/titles.csv'
    REVIEW = 'static/data/review.csv'
    COMMENT = 'static/data/comments.csv'
    GENRE_TITLE = 'static/data/genre_title.csv'
    MODELS = [Category, Genre, User, Title, Review, Comment]
    FILE_MODEL = {
        CATEGORY: Category,
        GENRE: Genre,
        USER: User,
        TITLE: Title,
        REVIEW: Review,
        COMMENT: Comment,
        GENRE_TITLE: Title
    }

    def write_base(self, url, model, csv):
        relations = get_field_info(model).forward_relations
        rel_fields = {}
        for field in csv.fieldnames:
            if (field in relations
                    and not relations[field].to_many):
                rel_fields[field] = relations[field].related_model
        for row in csv:
            try:
                if url == self.GENRE_TITLE:
                    genre = Genre.objects.get(
                        id=row.pop('genre_id'))
                    title = Title.objects.get(
                        id=row.pop('title_id'))
                    title.genre.add(genre)
                    title.save()
                else:
                    for field, r_model in rel_fields.items():
                        row[field] = r_model.objects.get(
                            id=row.get(field))
                    model.objects.create(**row)
            except Exception as err:
                print(f'Ошибка импорта файлов: {err}')

    def handle(self, *args, **options):
        for url, model in self.FILE_MODEL.items():
            path = f'{settings.BASE_DIR}/{url}'
            print(f'Начинается загрузка из {url}')
            try:
                with open(path, newline='', encoding='utf-8') as file:
                    csvfile = csv.DictReader(file, delimiter=',')
                    self.write_base(
                        url, model, csvfile
                    )
                print(f'Загрузка из {url} завершена.')
            except FileNotFoundError as err:
                print(f'Нет файла {url} в нужной дериктории: {err}')
