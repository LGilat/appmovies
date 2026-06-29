from functools import wraps
from hashlib import sha256
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

DEFAULT_TMDB_AUTHORIZATION = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYWEzMTMwNDQxNmE5ODk1NjI5NmViM2JjN2I5Mjc5YyIsIm5iZiI6MTcyNjQzMTMxNi41MTg1NDgsInN1YiI6IjY2ZTczYTAwZTgyMTFlY2QyMmIwYjRmNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rUmKSEIdbKNjtPLAxyDLU8ddaZ9z4AJc5vJ9jDj7KSE"
AUTHORIZATION = getattr(settings, "TMDB_AUTHORIZATION", None) or DEFAULT_TMDB_AUTHORIZATION
ACCEPT = "application/json"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_CACHE_TIMEOUT = 60 * 10
SEARCH_CACHE_TIMEOUT = 60 * 30


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def rate_limit(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        client_ip = get_client_ip(request)
        cache_key = f"rate_limit:{client_ip}"
        requests_count = cache.get(cache_key, 0)

        if requests_count >= 30:
            return HttpResponse("Too many requests", status=429)

        cache.set(cache_key, requests_count + 1, 60)
        return view_func(request, *args, **kwargs)

    return wrapped


def fetch_tmdb(endpoint, params=None, timeout=10):
    params = params or {}
    url = f"{TMDB_BASE_URL}/{endpoint.lstrip('/')}"
    if params:
        url = f"{url}?{urlencode(params)}"

    cache_key = f"tmdb:{url}"
    cached_payload = cache.get(cache_key)
    if cached_payload is not None:
        return cached_payload

    headers = {
        "accept": ACCEPT,
        "Authorization": AUTHORIZATION,
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    cache.set(cache_key, payload, TMDB_CACHE_TIMEOUT)
    return payload


@rate_limit
@cache_page(TMDB_CACHE_TIMEOUT)
def popular_movies(request):
    payload = fetch_tmdb("movie/popular", {"language": "en-US", "page": 1})
    movies = payload.get("results", [])
    return render(request, "movies/popular_movies.html", {"movies": movies})


@rate_limit
@cache_page(TMDB_CACHE_TIMEOUT)
def upcoming_movies(request):
    payload = fetch_tmdb("movie/upcoming", {"language": "en-US", "page": 1})
    movies = payload.get("results", [])
    return render(request, "movies/upcoming_movies.html", {"movies": movies})


@rate_limit
def search_movies(request):
    query = request.GET.get("query", "")
    normalized_query = " ".join(query.lower().strip().split())

    if len(normalized_query) < 2:
        return render(request, "movies/search_movies.html", {"movies": []})

    query_hash = sha256(normalized_query.encode("utf-8")).hexdigest()
    cache_key = f"search_movies:{query_hash}"
    movies = cache.get(cache_key)

    if movies is None:
        payload = fetch_tmdb(
            "search/movie",
            {
                "query": normalized_query,
                "include_adult": "false",
                "language": "en-US",
                "page": 1,
            },
        )
        movies = payload.get("results", [])
        cache.set(cache_key, movies, SEARCH_CACHE_TIMEOUT)

    return render(request, "movies/search_movies.html", {"movies": movies})


@rate_limit
@cache_page(TMDB_CACHE_TIMEOUT)
def nowplaying_movies(request):
    payload = fetch_tmdb("movie/now_playing", {"language": "en-US", "page": 1})
    movies = payload.get("results", [])
    return render(request, "movies/nowplaying_movies.html", {"movies": movies})


@rate_limit
@cache_page(TMDB_CACHE_TIMEOUT)
def movie_details(request, movie_id):
    movie_details = fetch_tmdb(f"movie/{movie_id}", {"language": "en-US"})
    credits = fetch_tmdb(f"movie/{movie_id}/credits", {"language": "en-US"})
    cast = credits.get("cast", [])
    return render(request, "movies/movie_details.html", {"movie": movie_details, "cast": cast})


def get_genres(request):
    payload = fetch_tmdb("genre/movie/list", {"language": "en"})
    return payload.get("genres", [])


@rate_limit
@cache_page(TMDB_CACHE_TIMEOUT)
def genre_movies(request, genre_id):
    payload = fetch_tmdb(
        "discover/movie",
        {
            "include_adult": "false",
            "include_video": "false",
            "language": "en-US",
            "page": 1,
            "sort_by": "popularity.desc",
            "with_genres": genre_id,
        },
    )
    movies = payload.get("results", [])
    return render(request, "movies/genre_movies.html", {"movies": movies})


@rate_limit
@cache_page(TMDB_CACHE_TIMEOUT)
def get_actor_films(request, actor_id):
    payload = fetch_tmdb(
        "discover/movie",
        {
            "include_adult": "false",
            "include_video": "false",
            "language": "en-US",
            "page": 1,
            "sort_by": "popularity.desc",
            "with_cast": actor_id,
        },
    )
    actor_details = fetch_tmdb(f"person/{actor_id}", {"language": "en-US"})
    movies = payload.get("results", [])
    return render(request, "movies/actor_movies.html", {"movies": movies, "actor_details": actor_details})


def index(request):
    return render(request, "movies/index.html")
