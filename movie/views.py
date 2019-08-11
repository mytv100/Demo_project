from django.http import HttpResponse, Http404
from django.shortcuts import render
import urllib.request
from urllib import parse
import json
import random

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
    context = {'movies': movies, 'genres': genre_list}
    return render(request, "movie/main.html", context)


def list(request, genre):
    # 장르별 출력
    movies = NewMovie.objects.filter(genre=genre)
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

    context = {'movies': movies, "genre": genre, 'contacts': contacts}
    return render(request, "movie/sidebar.html", context)


# 고객정보 넘겨주는거확인
def detail(request, movie_id, customer_id):
    try:
        movie = NewMovie.objects.get(pk=movie_id)
        customer = NewCustomer.objects.get(pk=customer_id)
    except NewMovie.objects.DoesNotExsit:
        raise Http404("Movie does not exist")

    str = customer.id + "/" + movie.id + "/"
    # query = urllib.parse.quote(str)
    # url = 'http://101.101.167.97:8000/movie-recommend/customerMovie/' + query + '/customer1/movie_list/'
    url = 'http://localhost:8000/movie-recommend/recommend' + str  # query

    content = urllib.request.urlopen(url).read().decode('utf-8')
    temp = json.loads(content)
    print(temp[0])
    recommend_list = []
    for i in range(20):
        recommend_list.append(temp[0][repr(i)])
        if repr(i + 1) not in temp[0]:
            break

    movie_list = []
    # 장르부분확인
    for j in recommend_list:
        if movie.genre in j['genre'] and len(movie_list) != 3:
            movie_list.append(j)

    for k in range(3 - len(movie_list)):
        choice = random.choice(recommend_list)
        if choice not in movie_list:
            movie_list.append(choice)

    return render(request, "movie/detail.html", {'movie': movie, 'recommended_movie': movie_list})


def column(request):
    return render(request, 'movie/4col.html')


def sidebar(request):
    return render(request, 'movie/sidebar.html')


def item(request):
    return render(request, 'movie/item.html')
