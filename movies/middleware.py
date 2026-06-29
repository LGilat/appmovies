from django.utils.cache import patch_cache_control


class CacheControlMiddleware:
    """Adds CDN-friendly cache headers for public movie pages only."""

    public_path_prefixes = ("/movies/",)
    public_paths = ("/",)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not self._should_add_shared_cache_header(request, response):
            return response

        patch_cache_control(
            response,
            s_maxage=600,
            stale_while_revalidate=600,
        )
        return response

    def _should_add_shared_cache_header(self, request, response):
        if request.method not in {"GET", "HEAD"}:
            return False

        if response.status_code != 200:
            return False

        if not self._is_public_movie_path(request.path):
            return False

        cache_control = response.get("Cache-Control", "").lower()
        if "private" in cache_control or "no-store" in cache_control:
            return False

        return True

    def _is_public_movie_path(self, path):
        return path in self.public_paths or path.startswith(self.public_path_prefixes)
