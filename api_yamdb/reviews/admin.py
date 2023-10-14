from django.contrib import admin
from django.db.models import Avg
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

admin.site.empty_value_display = 'Не задано'


class GenreResource(resources.ModelResource):
    """Ресурс для экспорта и импорта жанров."""

    class Meta:
        model = Genre


class GenreAdmin(ImportExportModelAdmin):
    """Администратор для модели Genre."""
    resource_classes = [GenreResource]
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


admin.site.register(Genre, GenreAdmin)


class CategoryResource(resources.ModelResource):
    """Ресурс для экспорта и импорта категорий."""

    class Meta:
        model = Category


class CategoryAdmin(ImportExportModelAdmin):
    """Администратор для модели Category."""
    resource_classes = [CategoryResource]
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


admin.site.register(Category, CategoryAdmin)


class TitleResource(resources.ModelResource):
    """Ресурс для экспорта и импорта произведений."""

    class Meta:
        model = Title


class TitleGenreInline(admin.TabularInline):
    model = TitleGenre
    extra = 2


class TitleAdmin(ImportExportModelAdmin):
    """Администратор для модели Title."""
    resource_classes = [TitleResource]
    list_display = ('name', 'year', 'get_rating',
                    'category', 'get_genres', 'description')
    list_filter = ('category', 'genre')
    search_fields = ('name', 'year', 'rating',
                     'category', 'genre', 'description')
    list_display_links = ('name',)
    inlines = (
        TitleGenreInline,
    )

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])

    get_genres.short_description = 'Жанр'

    def get_rating(self, obj):
        reviews = obj.review_set.all()
        average_score = reviews.aggregate(Avg('score'))['score__avg']
        return round(average_score) if average_score is not None else None

    get_rating.short_description = 'Рэйтинг'


admin.site.register(Title, TitleAdmin)


class TitleGenreResource(resources.ModelResource):
    """Ресурс для экспорта и импорта связей между произведениями и жанрами."""

    class Meta:
        model = TitleGenre


class TitleGenreAdmin(ImportExportModelAdmin):
    """Администратор для модели TitleGenre."""
    resource_classes = [TitleGenreResource]
    search_fields = ('title', 'genre')
    list_filter = ('genre',)


admin.site.register(TitleGenre, TitleGenreAdmin)


class ReviewResource(resources.ModelResource):
    """Ресурс для экспорта и импорта отзывов."""

    class Meta:
        model = Review


class ReviewAdmin(ImportExportModelAdmin):
    """Администратор для модели Review."""
    resource_classes = [ReviewResource]


admin.site.register(Review, ReviewAdmin)


class CommentResource(resources.ModelResource):
    """Ресурс для экспорта и импорта комментариев."""

    class Meta:
        model = Comment


class CommentAdmin(ImportExportModelAdmin):
    """Администратор для модели Comment."""
    resource_classes = [CommentResource]


admin.site.register(Comment, CommentAdmin)
