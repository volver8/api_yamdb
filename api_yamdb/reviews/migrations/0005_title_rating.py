# Generated by Django 3.2 on 2024-07-13 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.SmallIntegerField(default=1, verbose_name='Рейтинг произведения'),
            preserve_default=False,
        ),
    ]
