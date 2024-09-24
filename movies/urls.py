from django.urls import path 
from . import views

urlpatterns = [
    path('peliculas-populares/', views.popular_movies, name='popular_movies'),
    path('upcoming_movies/', views.upcoming_movies, name='upcoming_movies'),
    path('search/', views.search_movies, name='search_movies'),
    path('nowplaying/', views.nowplaying_movies, name='nowplaying_movies'),
    path('movie_details/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('genre_movies/<int:genre_id>/', views.genre_movies, name='genre_movies'),
]