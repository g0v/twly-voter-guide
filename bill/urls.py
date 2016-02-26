from django.conf.urls import url
from bill import views

urlpatterns = [
    url(r'^$', views.bills, name='bills'),
    url(r'^(?P<bill_id>\S+)/$', views.bill, name='bill'),
]
