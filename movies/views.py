from django.shortcuts import render

# Create your views here.
import requests

AUTHORIZATION = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYWEzMTMwNDQxNmE5ODk1NjI5NmViM2JjN2I5Mjc5YyIsIm5iZiI6MTcyNjQzMTMxNi41MTg1NDgsInN1YiI6IjY2ZTczYTAwZTgyMTFlY2QyMmIwYjRmNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rUmKSEIdbKNjtPLAxyDLU8ddaZ9z4AJc5vJ9jDj7KSE";
ACCEPT = "application/json"

def popular_movies(request):
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

    headers = {
        "accept": ACCEPT,
        "Authorization": AUTHORIZATION
    }
    
    response = requests.get(url, headers=headers)
    movies = response.json().get('results', [])
   
    return render(request, 'movies/popular_movies.html', {'movies': movies})
    

def upcoming_movies(request):
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1";
    headers = {
        "accept":ACCEPT,
        "Authorization": AUTHORIZATION,
    }
    
    response = requests.get(url, headers=headers);
    movies = response.json().get('results', []);
    return render(request, 'movies/upcoming_movies.html', {'movies': movies})


def search_movies(request):
    query = request.GET.get('query')
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": ACCEPT,
        "Authorization": AUTHORIZATION,
    }
    
    
    response = requests.get(url, headers=headers);
    movies = response.json().get('results', []);
    return render(request, 'movies/search_movies.html', {'movies': movies})


def nowplaying_movies(request):
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
    headers = {
        "accept": ACCEPT,
        "Authorization": AUTHORIZATION,
    }

    response = requests.get(url, headers=headers);
    movies = response.json().get('results', []);
    return render(request, 'movies/nowplaying_movies.html', {'movies': movies})


def movie_details(request, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    url_credits = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
    
    headers = {
        "accept": ACCEPT,
        "Authorization": AUTHORIZATION,
    }
    
    response = requests.get(url, headers=headers);
    movie_details = response.json();
    
    credits_response = requests.get(url_credits, headers=headers);
    cast = credits_response.json().get('cast', []);
    return render(request, 'movies/movie_details.html', {'movie': movie_details, 'cast': cast})


def get_genres(request):
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {
        "accept": ACCEPT,
        "Authorization": AUTHORIZATION,
    }
    response = requests.get(url, headers=headers)
    genres= response.json().get('genres', []);
    return genres;

def genre_movies(request, genre_id):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={genre_id}"
    headers = {
        "accept": ACCEPT,
        "Authorization": AUTHORIZATION,
    }
    response = requests.get(url, headers=headers)
    movies = response.json().get('results', []);
    return render(request, 'movies/genre_movies.html', {'movies': movies})


def get_actor_films(request, actor_id):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_cast={actor_id}"
    actor_details= f"https://api.themoviedb.org/3/person/{actor_id}?language=en-US"
    
    headers = {
        "accept": ACCEPT,
        "Authorization": AUTHORIZATION,
    }
    response = requests.get(url, headers=headers)
    actor_response = requests.get(actor_details, headers=headers)
    movies = response.json().get('results', []);
    actor_details = actor_response.json();
    return render(request, 'movies/actor_movies.html', {'movies': movies, 'actor_details': actor_details})

def index(request):
    return render(request, 'movies/index.html') 