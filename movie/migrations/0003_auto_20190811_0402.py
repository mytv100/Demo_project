# Generated by Django 2.2.1 on 2019-08-10 19:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_movie_movie_pk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewCustomer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(help_text='고객의 성별, M 남성, F 여성', max_length=32)),
                ('age', models.IntegerField(help_text='고객의 나이')),
                ('nickname', models.CharField(help_text='업체에서의 ID', max_length=64)),
                ('occupation', models.CharField(help_text='직업', max_length=128, null=True)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewMovie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='영화 제목', max_length=256)),
                ('description', models.CharField(default='Lorem ipsum dolor sit amet, consectetur adipiscing elit. ', help_text='영화 줄거리', max_length=256, null=True)),
                ('rate', models.FloatField(default=0.0, help_text='영화 평점')),
                ('votes', models.IntegerField(default=0, help_text='퍙점 투표수')),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('released_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('genre_set', models.ManyToManyField(to='movie.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=None, help_text='고객의 영화에 대한 평점')),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.NewCustomer')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.NewMovie')),
            ],
        ),
        migrations.AddField(
            model_name='newcustomer',
            name='movie',
            field=models.ManyToManyField(through='movie.Ratings', to='movie.NewMovie'),
        ),
    ]