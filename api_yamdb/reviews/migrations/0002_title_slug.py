# Generated by Django 3.2 on 2024-07-17 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='slug',
            field=models.SlugField(default=1, help_text='Идентификатор; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор'),
            preserve_default=False,
        ),
    ]