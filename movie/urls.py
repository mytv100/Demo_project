from django.urls import path

from movie import views

app_name = 'movie'
urlpatterns = [
    path('', views.index, name='index'),
    path('main', views.main, name='main'),

    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    # path('forgot_password', views.forgot_password, name='forgot_password'),

    path('<str:genre>/list', views.list, name='list'),
    path('<int:movie_id>/<int:customer_id>/', views.detail, name='detail'),

    path('column', views.column, name='column'),
    path('sidebar', views.sidebar, name='sidebar'),
    path('item', views.item, name='item'),
]
