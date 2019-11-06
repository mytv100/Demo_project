from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import urllib.request
import urllib.parse
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render

# Create your views here.

from movie.models import NewMovie, NewCustomer, Ratings, Genre

"""
# 장르 데이터
f = open('movie/module/data/ml-100k/u.genre', 'rb')
genre_list = []
for line in f.readlines():
    string = line.decode('ISO-8859-1')
    string_list = string.split('|')
    Genre.objects.create(name=string_list[0])
    genre_list.append(string_list[0])
    if string_list[0] == 'Western':
        break
f.close()

# url = 'http://101.101.167.97:8000/movie-recommend/businessPartnerMovie'
url = 'http://127.0.0.1:8000/movie-recommend/movie'
content = urllib.request.urlopen(url).read().decode('utf-8')
temp = json.loads(content)
for i in temp:
    if NewMovie.objects.filter(id=i['id']).exists():
        continue
    movie = NewMovie.objects.create(id=i['id'], title=i['title'],
                                    description=i['description'], rate=i['rate'], votes=i['votes'],
                                    released_date=i['released_date'])
    for genre in i['genre_set']:
        g = Genre.objects.get(name=genre)
        movie.genre_set.add(g)
url = 'http://127.0.0.1:8000/movie-recommend/customer'
content = urllib.request.urlopen(url).read().decode('utf-8')
temp = json.loads(content)
for i in temp:
    if NewCustomer.objects.filter(id=i['id']).exists():
        continue
    NewCustomer.objects.create(id=i['id'], age=i['age'], gender=i['gender'], occupation=i['occupation'])

# 평점 데이터
f = open('movie/module/data/ml-100k/u.data', 'rb')

for line in f.readlines():
    string = line.decode('ISO-8859-1')
    string_list = string.split("\t")
    Ratings.objects.create(customer_id=string_list[0], movie_id=string_list[1], rate=string_list[2])

f.close()

return render(None)


"""


def login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["lg_username"],
            password=request.POST["lg_password"])
        if user:
            auth.login(request, user)
            return redirect('movie:main')
    return render(request, 'movie/login.html')


def register(request):
    if request.method == "POST":
        if request.POST["reg_password"] == request.POST["reg_password_confirm"]:
            user = User.objects.create_user(
                username=request.POST["reg_username"],
                password=request.POST["reg_password"],
                email=request.POST['reg_email'], )

            nickname = request.POST["reg_nickname"]
            gender = request.POST['reg_gender']
            age = int(request.POST['reg_age'])
            profile = NewCustomer(user=user, nickname=nickname, gender=gender[0], age=age)
            profile.save()
            auth.login(request, user)
            return redirect('movie:main')
    return render(request, 'movie/register.html')


def forgot_password(request):
    return render(request, 'movie/register.html')


def index(request):
    movies = NewMovie.objects.order_by('-rate').order_by('-votes')[:4]
    context = {'movies': movies}
    return render(request, 'movie/index.html', context)


def main(request):
    genre_list = []
    genres = Genre.objects.values_list('name')
    for g in genres:
        genre_list.append(str(g).strip("(',')").strip('""'))
    genre_list.remove('unknown')

    movies = NewMovie.objects.order_by('-rate').order_by('-votes')[:6]
    context = {'movies': movies, 'genres': genre_list, 'customer': request.user}
    return render(request, "movie/main.html", context)


def list(request, genre):
    genre_list = []
    genres = Genre.objects.values_list('name')
    for g in genres:
        genre_list.append(str(g).strip("(',')").strip('""'))
    genre_list.remove('unknown')

    # 장르별 출력
    choiced_genre = Genre.objects.get(name=genre)
    movies = NewMovie.objects.filter(genre_set=choiced_genre)
    # item number per page
    num_page = 8
    paginator = Paginator(movies, num_page)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    context = {'movies': movies, "genre": choiced_genre, 'contacts': contacts, 'genres': genre_list,
               'customer': request.user}
    return render(request, "movie/sidebar.html", context)


# 고객정보 넘겨주는거확인
def detail(request, movie_id, customer_id):
    genre_list = []
    genres = Genre.objects.values_list('name')
    for g in genres:
        genre_list.append(str(g).strip("(',')").strip('""'))
    genre_list.remove('unknown')

    id = NewCustomer.objects.get(user=User.objects.get(id=customer_id)).id
    movie = NewMovie.objects.get(id=movie_id)
    string = str(id) + "/" + str(movie_id) + "/"
    # query = urllib.parse.quote(string)
    # url = 'http://101.101.167.97:8000/movie-recommend/customerMovie/' + query + '/customer1/movie_list/'
    url = 'http://localhost:8000/movie-recommend/recommend/' + string  # query

    content = urllib.request.urlopen(url).read().decode('utf-8')
    temp = json.loads(content)
    recommend_list = []
    for i in range(len(temp[0])):
        recommend_list.append(temp[0][repr(i)])

    movie_list = []

    for j in recommend_list:
        m = NewMovie.objects.get(id=j['movie_id'])
        movie_list.append(m)

    return render(request, "movie/detail.html",
                  {'genres': genre_list, 'movie': movie, 'recommended_movie': movie_list, 'customer': request.user})


def column(request):
    return render(request, 'movie/4col.html')


def sidebar(request):
    return render(request, 'movie/sidebar.html')


def item(request):
    return render(request, 'movie/item.html')
