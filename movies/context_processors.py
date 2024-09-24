
from .views import get_genres

def genres_processor(request):
    return {'genres': get_genres(request)}
