from django.http import HttpResponse, Http404
from django.shortcuts import render
import urllib.request
from urllib import parse
import json
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render

from django.views import View

# Create your views here.
from movie.models import Customer, Movie, CustomerMovie

""" 
Movie.objects.all().delete()
    url = 'http://101.101.167.97:8000/movie-recommend/businessPartnerMovie'
    content = urllib.request.urlopen(url).read().decode('utf-8')
    temp = json.loads(content)
    for i in temp:
        if Movie.objects.filter(title=i['title'], director=i['director']).exists():
            continue
        Movie.objects.create(movie_pk=i['movie_pk'],title=i['title'], genre=i['genre'],
                             description=i['description'], rate=i['rate'], votes=i['votes'],
                             running_time=i['running_time'], director=i['director'])

    url2 = 'http://101.101.167.97:8000/movie-recommend/customerMovie'
    content = urllib.request.urlopen(url2).read().decode('utf-8')
    temp = json.loads(content)
    for i in temp:
        movie = Movie.objects.get(title=i['title'], director=i['director'])
        customer = Customer.objects.get(nickname=i['nickname'])
        CustomerMovie.objects.create(movie_id=movie.id, customer_id=customer.id, rate=i['rate'])

url = "http://101.101.167.97:8000/movie-recommend/customer/"
    # url = "http://101.101.167.97:8000/api/doc/"
    content = urllib.request.urlopen(url).read().decode('utf-8')
    # # str -> list
    temp = json.loads(content)
    gender = 0
    for i in temp:
        if i['gender'] == 'man':
            gender = True
        else:
            gender = False
        Customer.objects.create(gender=gender, age=i['age'], nickname=i['nickname'])
        
    
"""


def index(request):
    movies = Movie.objects.order_by('-votes').order_by('-rate')[:4]
    context = {'movies': movies}
    return render(request, 'movie/index.html', context)


def main(request):
    movies = Movie.objects.order_by('-votes').order_by('-rate')[:6]
    context = {'movies': movies}
    return render(request, "movie/main.html", context)


def list(request, genre):
    movies = Movie.objects.filter(genre=genre)
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


def detail(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.objects.DoesNotExsit:
        raise Http404("Movie does not exist")

    str = movie.title + "/" + movie.director
    query = urllib.parse.quote(str)
    # url = 'http://101.101.167.97:8000/movie-recommend/customerMovie/' + query + '/customer1/movie_list/'
    url = 'http://localhost:8000/movie-recommend/customerMovie/' + query + '/customer1/movie_list/'



    content = urllib.request.urlopen(url).read().decode('utf-8')
    temp = json.loads(content)
    print(temp[0])
    recommend_list = []
    for i in range(20):
        recommend_list.append(temp[0][repr(i)])
        if repr(i + 1) not in temp[0]:
            break

    movie_list = []
    for j in recommend_list:
        if movie.genre in j['genre'] and len(movie_list)!=3:
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
