from django.contrib import admin

from reviews.models import Categories, Genres, Titles


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
