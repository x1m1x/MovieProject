from django import template

from movies.models import Category, Movie, Genre

register = template.Library()

@register.simple_tag
def get_categories():
    categories = Category.objects.all()
    return categories

@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count=5):
    last_movies = Movie.objects.order_by('id')[:count]
    return {"last_movies": last_movies}
