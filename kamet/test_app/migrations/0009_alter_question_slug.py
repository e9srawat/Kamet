# Generated by Django 4.2.11 on 2024-03-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0008_question_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(max_length=6, unique=True),
        ),
    ]
