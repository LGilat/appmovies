# AppMovies

AppMovies is a Django web application for discovering movie information from [The Movie Database (TMDB)](https://www.themoviedb.org/). It includes pages for popular films, upcoming releases, movies currently in theaters, genre-based discovery, actor filmographies, search, and detailed movie information.

## Portfolio Highlights

- **Django 4.2 application** with reusable templates and a simple, maintainable project structure.
- **TMDB integration** for real movie data, credits, actors, genres, and discovery pages.
- **Production hardening for serverless hosting** with in-memory caching, request throttling, and CDN-friendly cache headers.
- **Optimized search flow** that rejects very short queries and caches normalized query results to reduce external API usage.
- **Vercel-ready configuration** for lightweight deployment.

## Features

- Browse popular movies.
- Browse upcoming releases.
- Browse movies currently playing.
- Search movies by title.
- View movie details and cast.
- Browse movies by genre.
- Browse movies by actor.

## Performance and Stability Improvements

This project is hardened to avoid excessive TMDB usage and unnecessary serverless invocations:

- Django `LocMemCache` is configured globally.
- TMDB-backed views use a 10-minute page cache.
- TMDB HTTP requests are centralized in a `fetch_tmdb()` helper.
- TMDB API responses are cached by endpoint and query string.
- Search queries shorter than two characters do not call TMDB.
- Search results are cached for 30 minutes using a normalized query key.
- Basic IP rate limiting blocks requests above 30 requests per minute.
- Responses include `Cache-Control: s-maxage=600, stale-while-revalidate` for edge caching.

## Tech Stack

- Python
- Django 4.2
- Requests
- Bootstrap templates
- TMDB API
- Vercel deployment support

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd appmovies
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure TMDB credentials

Set a TMDB API read token as an environment variable:

```bash
export TMDB_AUTHORIZATION="Bearer <your-tmdb-read-token>"
```

> The application includes a fallback token for the existing project configuration, but a personal TMDB token is recommended for production deployments.

### 5. Run the development server

```bash
python manage.py runserver
```

Open the app at:

```text
http://127.0.0.1:8000/
```

## Deployment Notes

For Vercel or another serverless platform:

1. Add `TMDB_AUTHORIZATION` as an environment variable.
2. Keep the cache in memory unless external infrastructure is intentionally introduced.
3. Use the provided cache headers to allow CDN-level caching.
4. Monitor TMDB API usage after deployment.

## Project Structure

```text
appmovies/          Django project settings and URL configuration
movies/             Movie app views, templates, middleware, and routing
templates/          Shared project templates
static/             Static assets
vercel.json         Vercel deployment configuration
requirements.txt    Python dependencies
```

## Security and API Usage

This app is designed for portfolio and demonstration use. Before using it in a high-traffic production environment, review secret management, Django `DEBUG`, allowed hosts, and persistent cache options based on your hosting requirements.

## License

This project is intended for educational and portfolio purposes.
