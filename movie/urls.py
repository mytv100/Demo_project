from django.urls import path

from movie import views

app_name = 'movie'
urlpatterns = [
    path('', views.index, name='index'),
    path('main', views.main, name='main'),
    path('<str:genre>/list', views.list, name='list'),
    path('<int:movie_id>/', views.detail, name='detail'),

    path('column',views.column, name='column'),
    path('sidebar',views.sidebar, name='sidebar'),
    path('item',views.item, name='item'),
]
