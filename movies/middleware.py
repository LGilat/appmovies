class CacheControlMiddleware:
    """Adds CDN-friendly cache headers for Vercel and other edge caches."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cache-Control"] = "s-maxage=600, stale-while-revalidate"
        return response
