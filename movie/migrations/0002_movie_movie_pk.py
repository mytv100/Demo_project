# Generated by Django 2.2.1 on 2019-06-23 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_pk',
            field=models.CharField(help_text='영화의 PrimaryKey', max_length=64, null=True),
        ),
    ]
