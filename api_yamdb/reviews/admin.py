from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Category, Genre, TitleGenre, Title, Review, Comment


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


admin.site.register(Genre, GenreAdmin)


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


admin.site.register(Category, CategoryAdmin)


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title


class TitleGenreInline(admin.TabularInline):
    model = TitleGenre
    extra = 2


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    list_display = ('name', 'year', 'rating',
                    'category', 'get_genres', 'description')
    list_filter = ('category', 'genre')
    search_fields = ('name', 'year', 'rating',
                     'category', 'genre', 'description')
    list_display_links = ('name',)
    inlines = (
        TitleGenreInline,
    )

    def get_genres(self, obj):
        return ' '.join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = 'Жанр'


admin.site.register(Title, TitleAdmin)


class TitleGenreResource(resources.ModelResource):

    class Meta:
        model = TitleGenre


class TitleGenreAdmin(ImportExportModelAdmin):
    resource_classes = [TitleGenreResource]
    search_fields = ('title_id', 'genre_id')
    list_filter = ('genre_id',)


admin.site.register(TitleGenre, TitleGenreAdmin)


class ReviewResource(resources.ModelResource):

    class Meta:
        model = Review


class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]


admin.site.register(Review, ReviewAdmin)


class CommentResource(resources.ModelResource):

    class Meta:
        model = Review


class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]


admin.site.register(Comment, CommentAdmin)


admin.site.empty_value_display = 'Не задано'
