# -*- coding: utf-8 -*-
from django.conf import settings
from committees.models import Legislator_Committees


def current_url(request):
        return {'current_url': settings.SITE_DOMAIN+request.get_full_path()}
def last_update_time(request):
        return {'last_update_time':'2013-11-01'}
def district_list(request):
        return {'district_list':["山地原住民","台中市","台北市","台東縣","台南市","平地原住民","全國不分區","宜蘭縣","花蓮縣","金門縣","南投縣","屏東縣","苗栗縣","桃園縣","高雄市","基隆市","連江縣","雲林縣","新北市","新竹市","新竹縣","僑居國外國民","嘉義市","嘉義縣","彰化縣","澎湖縣"]}
def committee_list(request):
        return {'committee_list':Legislator_Committees.objects.filter(ad=8).values_list('committee', flat=True).distinct('committee')}
