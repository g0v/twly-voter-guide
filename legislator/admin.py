from django.contrib import admin
from legislator.models import Legislator
from search.models import Keyword


class KeywordAdmin(admin.ModelAdmin):
    fieldsets = [
            ('keyword', {'fields':['content']}),
            ('category', {'fields':['category']}),
            ('valid', {'fields':['valid']}),
            ('hits', {'fields':['hits']})
            ]
    list_display = ('content', 'category', 'valid', 'hits')
    list_filter = ['category']
    search_fields = ['content']

class LegislatorAdmin(admin.ModelAdmin):
    fieldsets = [
            ('name', {'fields':['name']}),
            ]
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Legislator, LegislatorAdmin)
