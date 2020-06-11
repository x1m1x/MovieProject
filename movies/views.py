from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.views.generic import View
from django.views.generic import ListView, DetailView

from django.db.models import Q
from django.core.paginator import Paginator

from .models import *
from .forms import ReviewForm, RatingForm



class GenreYear:
    def get_years(self):
        movies = Movie.objects.filter(draft=False).values('year')
        return movies

    def get_genres(self):
        return Genre.objects.all()

    def get_rating(self):
        return RatingStar.objects.all()

class MoviesView(GenreYear, ListView):
    model = Movie
    count = 6

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = Movie.objects.filter(title__icontains=search_query, draft=False)
        else:
            queryset = Movie.objects.filter(draft=False)
        return queryset

    paginate_by = count



class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "url"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()

        return redirect(movie.get_absolute_url())


class ActorDetailView(GenreYear, DetailView):
    model = Actor
    template_name = "movies/actor_detail.html"
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    def get_rating_id(self):
        try:
            rating = RatingStar.objects.get(value=self.request.GET.get('rating_star') ).rating_set.get().id
            return rating
        except:
            return 0



    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres=self.request.GET.get('genre')) |
            Q(rating=self.get_rating_id()) |
            Q(category=self.request.GET.get('category') ) )

        return queryset.distinct()


class CategoryFilter(GenreYear, ListView):
    def get_queryset(self):
        return Movie.objects.filter(category=Category.objects.get(name=self.request.GET.get('category')))


class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
