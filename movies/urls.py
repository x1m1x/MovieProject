from django.urls import path

from .views import *

urlpatterns = [
    path('', MoviesView.as_view(), name="movies_list_url"),
    path('filter/', FilterMoviesView.as_view(), name = "filter_movies_url"),
    path('add_rating/', AddStarRating.as_view(), name="add_star_rating_url"),
    path('<str:slug>/', MovieDetailView.as_view(), name="movie_detail_url"),
    path('review/<int:pk>/', AddReview.as_view(), name="add_review_url"),
    path('actor/<str:slug>/', ActorDetailView.as_view(), name="actor_detail_url"),
]
