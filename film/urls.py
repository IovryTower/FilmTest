
from django.urls import path, re_path
from . import views
from . import set_film_data
from . import  new_film

urlpatterns = [
    path('hell/', views.hell),  # views.py
    path('search_film/', views.search_film),
    path('search/', views.search),
    # path('get_all/', views.get_all),
    # path('insert_film_tag/', views.insert_film_tag),
    # path('insert/', views.insert),

    path('film_type/', views.film_type),
    path('films/', views.films),
    path('film_info/', views.film_info),

    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('search2/', views.search2),
    path('logout/', views.logout),
    path('user_page/', views.user_page),
    path('others_page/', views.others_page),

    path('recommend/', views.recommend),

    path('start_film/', set_film_data.start_film),

    path('ranking/', new_film.ranking),
    path('last_film/', new_film.last_film),
    path('unpopular/', new_film.unpopular),
    path('encounter/', new_film.encounter),
    path('high/', new_film.high),
    path('manage/', new_film.manage),

]
