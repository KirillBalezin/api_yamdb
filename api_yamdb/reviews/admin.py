from django.contrib import admin

from .models import Categories, Genres, Titles, Review, Comment


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Review)
admin.site.register(Comment)
