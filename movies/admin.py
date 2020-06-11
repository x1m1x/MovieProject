from django.contrib import admin
from django.utils.safestring import mark_safe

from django import forms

from .models import *

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name', )


class ReviewInline(admin.StackedInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email', )


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image', )
    def get_image(self, obj):
        return mark_safe('<img src={} width="100" height="110"'.format(obj.image.url))

    get_image.short_description = "Изображение"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name', )
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ['draft']
    readonly_fields = ('get_image', )
    form = MovieAdminForm

    def get_image(self, obj):
        return mark_safe('<img src={} width="{}" height="{}"'.format(obj.poster.url, obj.poster.width//2, obj.poster.height//2))

    get_image.short_description = "Изображение"

    fieldsets = (
        ("Titles", {
            'fields': (('title', 'tagline'), )
        }),
        ("Description/poster", {
            'fields': ('description', 'poster', 'get_image')
        }),
        ("Premiere", {
            'fields': (('year', 'world_premiere', 'country'), )
        }),
        ("Actors/directors/genres/category", {
            'classes': ('collapse', ),
            'fields': (('actors', 'directors', 'genres', 'category'), )
        }),
        ("Budget/fees", {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'), )
        }),
        ("Options", {
            'fields': (('url', 'draft'), )
        }),
    )

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    search_fields = ('name', 'age')
    list_filter = ('age', )
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe('<img src={} width="50" height="60"'.format(obj.image.url))

    get_image.short_description = "Изображение"

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe('<img src={} width="100" height="60"'.format(obj.image.url))

    get_image.short_description = "Изображение"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'ip')

@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value', )


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
