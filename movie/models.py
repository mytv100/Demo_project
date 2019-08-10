from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import CreationDateTimeField


class NewMovie(models.Model):
    """
    영화 데이터
    id PrimaryKey
    title 제목
    description 줄거리
    rate 평점
    votes 투표수
    created_at 이 객체가 생성된 시간
    released_date 개봉 날짜
    movie_owner 이 영화를 가지고 있는 업체 (ManyToManyField 로 through 클래스로 구현)
    genre_set ManyToManyField(to='Genre')

    """
    id: int = models.AutoField(
        primary_key=True
    )

    title: str = models.CharField(
        help_text="영화 제목",
        max_length=256,
        null=False,
    )

    description: str = models.CharField(
        help_text="영화 줄거리",
        max_length=256,
        null=True,
        default="Lorem ipsum dolor sit amet, "
                "consectetur adipiscing elit. ",
    )

    rate: float = models.FloatField(
        help_text="영화 평점",
        default=0.0,
    )
    votes: int = models.IntegerField(
        help_text="퍙점 투표수",
        default=0,
    )

    # 생성된 날짜, 시간
    created_at: datetime = CreationDateTimeField()
    # 개봉 날짜
    released_date: datetime = models.DateTimeField(default=timezone.now)

    genre_set = models.ManyToManyField(to='Genre')


class Genre(models.Model):
    name = models.CharField(max_length=32, null=False)
    created_at: datetime = CreationDateTimeField()


class NewCustomer(models.Model):
    """
    고객 데이터 (업체의 고객)
    id PK
    gender 성별 M 남성, F 여성
    age 나이
    nickname 아이디, 닉네임
    created_at 이 객체가 생성된 시간
    occupation 직업
    """
    id: int = models.AutoField(
        primary_key=True
    )
    gender: str = models.CharField(
        help_text="고객의 성별, M 남성, F 여성",
        max_length=32
    )

    age: int = models.IntegerField(
        help_text="고객의 나이",
        null=False
    )

    nickname: str = models.CharField(
        help_text="업체에서의 ID",
        max_length=64,
        null=False,
    )

    occupation: str = models.CharField(
        help_text='직업',
        max_length=128,
        null=True
    )
    created_at: datetime = CreationDateTimeField()

    movie: NewMovie = models.ManyToManyField(
        NewMovie,
        through='Ratings',
    )


class Ratings(models.Model):
    """
    고객과 영화 사이의 M2M 클래스 ( 고객이 평가한 영화 )
    customer 고객
    movie 영화
    rate 평점
    created_at 이 객체가 생성된 시간
    """

    customer: NewCustomer = models.ForeignKey(
        NewCustomer,
        on_delete=models.CASCADE
    )

    movie: NewMovie = models.ForeignKey(
        NewMovie,
        on_delete=models.CASCADE
    )

    rate: float = models.FloatField(
        help_text="고객의 영화에 대한 평점",
        null=False,
        default=None
    )

    created_at: datetime = CreationDateTimeField()


# Create your models here.
class Customer(models.Model):
    gender = models.BooleanField()
    age = models.IntegerField(null=False)
    nickname = models.CharField(max_length=64)

    def __str__(self):
        return self.nickname


class Movie(models.Model):
    movie_pk: str = models.CharField(
        help_text="영화의 PrimaryKey",
        max_length=64,
        null=True,
    )

    title = models.CharField(
        max_length=256,
        null=False
    )

    genre = models.CharField(max_length=256)

    description = models.CharField(
        max_length=256,
        null=True,
        default="Lorem ipsum dolor sit amet, "
                "consectetur adipiscing elit. "
                "Nam eget consequat eros, a lacinia turpis. "
                "Phasellus faucibus commodo diam"
    )

    rate = models.FloatField(default=0.0)
    votes = models.IntegerField(default=0)
    running_time = models.IntegerField(default=0)
    director = models.CharField(max_length=256)
    actor = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class CustomerMovie(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    )

    rate = models.FloatField(null=False, default=0.0)

    def __str__(self):
        return self.customer.nickname + " : " + self.movie.title
