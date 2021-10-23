from django.contrib import admin

from .models import Category, Comment, CustomUser, Genre, Review, Title


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'year',)
    raw_id_fields = ('genre',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score', 'pub_date',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'username', 'bio',
                    'email', 'role', 'password')
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Genre, GenresAdmin)
admin.site.register(Category, CategoriesAdmin)
