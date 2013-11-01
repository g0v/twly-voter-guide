from django.contrib import admin
from legislator.models import Legislator
from search.models import Keyword
from issue.models import Issue


class IssueAdmin(admin.ModelAdmin):
    fieldsets = [
        ('title', {'fields':['title']}),
        ('content', {'fields':['content']}),      
        ('date', {'fields':['date']}),
        ('hits', {'fields':['hits']}),
        ('reference', {'fields':['reference']})
    ]
    list_display = ('title','date','hits', 'reference')
    list_filter = ['date']
    search_fields = ['title']

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
          ('party', {'fields':['party']}),
          ('enable', {'fields':['enable']}),
          ('disableReason', {'fields':['disableReason']}),
          ('hits', {'fields':['hits']}),
          ('facebook', {'fields':['facebook']}),
          ('wiki', {'fields':['wiki']})
    ]
    list_display = ('name','party','hits','enable')
    list_filter = ['enable']
    search_fields = ['name']

admin.site.register(Issue, IssueAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Legislator, LegislatorAdmin)
