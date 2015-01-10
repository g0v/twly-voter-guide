# -*- coding: utf-8 -*-
import operator
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F, Q
from django.forms.models import model_to_dict

from haystack.query import SearchQuerySet

from .models import LegislatorDetail
from vote.models import Vote
from bill.models import Bill
from sittings.models import Sittings
from committees.models import Legislator_Committees
from search.views import keyword_list, keyword_normalize


def get_legislator(legislator_id, ad):
    try:
        return LegislatorDetail.objects.select_related().get(ad=ad, legislator_id=legislator_id)
    except Exception, e:
        print e

def index(request, index, ad):
    query = Q(ad=ad, in_office=True)
    outof_ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=False)
    if index == 'conscience_vote':
        ly_list = LegislatorDetail.objects.filter(query, votes__conflict=True)\
                                          .annotate(totalNum=Count('votes__id'))\
                                          .order_by('-totalNum','party')
        no_count_list = LegislatorDetail.objects.filter(query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True)).order_by('party')
        return render(request,'legislator/index/index_ordered.html', {'ad':ad,'no_count_list':no_count_list,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index})
    elif index == 'notvote':
        ly_list = LegislatorDetail.objects.filter(query, votes__decision__isnull=True)\
                                          .annotate(totalNum=Count('votes__id'))\
                                          .exclude(totalNum=0)\
                                          .order_by('-totalNum','party')
        no_count_list = LegislatorDetail.objects.filter(query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True))
        return render(request,'legislator/index/index_ordered.html', {'ad':ad,'no_count_list':no_count_list,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index})

def committees(request, ad):
    ly_list = Legislator_Committees.objects.select_related()\
                                           .filter(ad=ad, in_office=True)\
                                           .order_by('committee', 'session', 'legislator__party', 'legislator__name')
    outof_ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=False)
    return render(request, 'legislator/index/committees.html', {'ad': ad, 'ly_list': ly_list, 'outof_ly_list': outof_ly_list})

def counties(request, ad):
    ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=True)\
                                      .order_by('-county', 'party')
    outof_ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=False)
    return render(request, 'legislator/index/countys.html', {'ad': ad, 'ly_list': ly_list, 'outof_ly_list': outof_ly_list})

def county(request, county, ad):
    ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=True, county=county)\
                                      .order_by('party', 'name')
    return render(request, 'legislator/county.html', {'ad': ad, 'ly_list': ly_list, 'county': county})

def committee(request, committee, ad):
    ly_list = Legislator_Committees.objects.select_related('legislator').filter(ad=ad, legislator__in_office=True, committee=committee).order_by('-session', 'legislator__party', 'legislator__name')
    return render(request, 'legislator/committee.html',  {'ly_list': ly_list, 'committee': committee})

def personal_political_contributions(request, legislator_id, ad):
    ly = get_object_or_404(LegislatorDetail.objects.select_related('politicalcontributions'), ad=ad, legislator_id=legislator_id)
    try:
        pc = ly.politicalcontributions.get()
        data_income = model_to_dict(pc, fields=["in_individual", "in_profit", "in_party", "in_civil", "in_anonymous", "in_others"])
        data_expenses = model_to_dict(pc, fields=["out_personnel", "out_propagate", "out_campaign_vehicle", "out_campaign_office", "out_rally", "out_travel", "out_miscellaneous", "out_return", "out_exchequer", "out_public_relation"])
        data_total = model_to_dict(pc, fields=["in_total", "out_total"])
    except:
        raise Http404
    return render(request, 'legislator/personal_politicalcontributions.html', {'ly': ly, 'data_total': data_total, 'data_income': data_income, 'data_expenses': data_expenses})

def voter_detail(request, legislator_id, ad, index):
    ly = get_object_or_404(LegislatorDetail.objects.select_related('votes'), ad=ad, legislator_id=legislator_id)

    qs = Q(conflict=True) if index == 'conscience' else Q()
    if 'decision' in request.GET:
        decisions = {"agree": Q(decision=1), "disagree": Q(decision=-1), "abstain": Q(decision=0), "notvote": Q(decision__isnull=True)}
        qs = qs & decisions.get(request.GET['decision'], Q())
    if request.GET.get('keyword'):
        sqs = SearchQuerySet().filter(content=request.GET['keyword']).models(Vote)
        votes = ly.votes.select_related().filter(qs & Q(vote_id__in=[x.uid for x in sqs]))
    else:
        votes = ly.votes.select_related().filter(qs)
    keywords = keyword_list(2)
    return render(request, 'legislator/voter_detail.html', {'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'ly': ly, 'index': index, 'votes': votes, 'keyword': request.GET.get('keyword')})

def biller_detail(request, legislator_id, ad):
    ly = get_object_or_404(LegislatorDetail.objects.select_related('bills'), ad=ad, legislator_id=legislator_id)
    bills = ly.bills.filter(legislator_id=ly.id, priproposer=True)
    qs = Q(uid__in=bills.values_list('bill_id', flat=True))
    qs = qs & Q(content=request.GET['keyword']) if request.GET.get('keyword') else qs
    bills = SearchQuerySet().filter(qs).models(Bill).order_by('-last_action_at')
    keywords = keyword_list(3)
    return render(request, 'legislator/biller_detail.html',  {'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'bills': bills, 'ly': ly, 'keyword': request.GET.get('keyword')})

def platformer_detail(request, legislator_id, ad):
    ly = get_object_or_404(LegislatorDetail, ad=ad, legislator_id=legislator_id)
    return render(request, 'legislator/platformer.html', {'ly': ly})

def chart_report(request, ad, index='vote'):
    ly_obj, ly_name, vote_obj, title, content, compare, data = [], [], [], None, None, None, None
    ad = ad or 8
    if index == 'vote':
        compare = Vote.objects.filter(sitting__ad=ad).count()
        ly_obj = LegislatorDetail.objects.filter(ad=ad, in_office=True, votes__decision__isnull=True).annotate(totalNum=Count('votes__id')).order_by('-totalNum','party')[:10]
        title, content = u'立法院表決缺席前十名', u'可和立法院開會缺席交叉比較，為何開會有出席但沒有參加表決？(點選立委名字可看立委個人投票紀錄)'
    elif index == 'conscience_vote':
        compare = Vote.objects.filter(sitting__ad=ad).count()
        ly_obj = LegislatorDetail.objects.filter(ad=ad, in_office=True, votes__conflict=True).annotate(totalNum=Count('votes__id')).order_by('-totalNum','party')[:10]
        title, content = u'脫黨投票次數前十名', u'脫黨投票不一定較好，可能該立委是憑良心投票，也可能是受財團、企業影響所致，還請點選該立委觀看其脫黨投票的表決內容再作論定。'
    elif index == 'biller':
        compare = "{0:.2f}".format(Bill.objects.count()/116.0)
        ly_obj = LegislatorDetail.objects.filter(ad=8, in_office=True, bills__priproposer=True, bills__petition=False).annotate(totalNum=Count('bills__id')).order_by('-totalNum','party')[:10]
        title, content = u'法條修正草案數前十名', u'量化數據不能代表好壞只能參考，修正草案數多不一定較好，還請點選該立委觀看其修正草案的內容再作論定。'
    elif index == 'ly':
        compare = Sittings.objects.filter(ad=ad, committee='').count()
        ly_obj = LegislatorDetail.objects.filter(ad=ad, in_office=True, attendance__category='YS', attendance__status='absent').annotate(totalNum=Count('attendance__id')).order_by('-totalNum','party')[:10]
        title, content = u'立法院開會缺席前十名', u'立委須參加立法院例行會議，在會議中進行質詢、法案討論表決、人事表決等重要工作(點選立委名字可看立委投票紀錄)'
    return render(request,'legislator/chart_report.html', {'compare':compare,'ad':ad,'title':u'%s(第%s屆)' %(title, ad),'content':content,'index':index,'vote_obj':vote_obj,'ly_name': [ly.name for ly in ly_obj],'ly_obj':ly_obj, 'data': list(ly_obj.values('name', 'totalNum'))} )

def political_contributions_report(request, index='in_party', compare='conscience_vote', party=u'中國國民黨'):
    ly_obj, title, content, data = [], None, None, None
    pc_field = {
        "in_individual": u'個人捐贈收入',
        "in_profit": u'營利事業捐贈收入',
        "in_party": u'政黨捐贈收入',
        "in_civil": u'人民團體捐贈收入',
        "in_anonymous": u'匿名捐贈收入',
        "in_others": u'其他收入',
        "in_total": u'收入合計',
        "out_personnel": u'人事費用支出',
        "out_propagate": u'宣傳支出',
        "out_campaign_vehicle": u'租用宣傳車輛支出',
        "out_campaign_office": u'租用競選辦事處支出',
        "out_rally": u'集會支出',
        "out_travel": u'交通旅運支出',
        "out_miscellaneous": u'雜支支出',
        "out_return": u'返還捐贈支出',
        "out_exchequer": u'繳庫支出',
        "out_public_relation": u'公共關係費用支出',
        "out_total": u'支出合計',
        "balance": u'收支平衡'
    }
    index_field = {
        "conscience_vote": {
            "legend": u'脫黨投票次數',
            "query": 'SELECT COUNT(*) FROM vote_legislator_vote WHERE vote_legislator_vote.conflict=True AND vote_legislator_vote.legislator_id = legislator_legislatordetail.id GROUP BY vote_legislator_vote.legislator_id'
        },
        "vote": {
            "legend": u'表決缺席次數',
            "query": 'SELECT COUNT(*) FROM vote_legislator_vote WHERE vote_legislator_vote.decision isnull AND vote_legislator_vote.legislator_id = legislator_legislatordetail.id GROUP BY vote_legislator_vote.legislator_id'
        },
        "biller": {
            "legend": u'法條修正草案數',
            "query": 'SELECT COUNT(*) FROM bill_bills WHERE bill_bills.priproposer=True AND bill_bills.petition=False AND bill_bills.legislator_id = legislator_legislatordetail.id GROUP BY bill_bills.legislator_id'
        }
    }
    filter_dict = {
        "ad": 8,
        "party": party,
        "politicalcontributions__%s__isnull" % index: False
    }
    if pc_field.get(index) and index_field.get(compare):
        legend = [pc_field.get(index), index_field.get(compare).get('legend'), 'money', 'count']
        ly_obj = LegislatorDetail.objects.filter(**filter_dict)\
                                         .annotate(totalNum=Sum('politicalcontributions__%s' % index))\
                                         .order_by('-totalNum')\
                                         .extra(select={'compare': index_field.get(compare).get('query')},)
    elif pc_field.get(index) and pc_field.get(compare):
        legend = [pc_field.get(index), pc_field.get(compare), 'money', 'money']
        ly_obj = LegislatorDetail.objects.filter(**filter_dict)\
                                         .annotate(totalNum=Sum('politicalcontributions__%s' % index))\
                                         .order_by('-totalNum')\
                                         .annotate(compare=Sum('politicalcontributions__%s' % compare))
    return render(request,'legislator/chart_report_for_political_contribution.html', {'compare':compare,'legend':legend,'party':party,'index':index,'ly_name': [ly.name for ly in ly_obj],'ly_obj':ly_obj,'data':list(ly_obj.values('name', 'totalNum', 'compare')),'pc_field':sorted(pc_field.items()),'index_field':index_field})
