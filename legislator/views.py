# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.db import connections
from django.db.models import Count, Q
from django.forms.models import model_to_dict

from haystack.query import SearchQuerySet

from .models import LegislatorDetail
from vote.models import Vote
from bill.models import Bill
from sittings.models import Sittings
from committees.models import Legislator_Committees
from search.models import Keyword
from standpoint.models import Standpoint
from search.views import keyword_list, keyword_normalize


def index(request, index, ad):
    outof_ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=False)
    maps = {
        'conflict': {
            'title': u'脫黨投票',
            'description': u'<h4><p>脫黨投票：立委表決的決定與所屬政黨多數意見不同。</p><small>脫黨投票不一定較好，可能該立委是憑良心投票，也可能是受財團、企業影響所致，還請點選該立委觀看其脫黨投票的表決內容再作論定。</small>',
            'url_class': 'legislator:voter_detail',
            'index': 'conscience',
        },
        'not_voting': {
            'title': u'投票缺席',
            'description': u'',
            'url_class': 'legislator:voter_detail',
            'index': '',
        },
    }
    ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=True)\
                                      .extra(select={
                                          'count': "COALESCE(cast(vote_param::json->>'%s' as int), 0)" % index,
                                          'percentage': "COALESCE(round(cast(cast(vote_param::json->>'%s' as float)/cast(vote_param::json->>'total' as float)*100 as numeric), 2), 0)" % index,
                                          'ranking': "COALESCE(floor(cast(vote_param::json->>'%s' as float)/cast(vote_param::json->>'total' as float)*10)*10, 0.0)" % index,
                                      },)\
                                      .order_by('-percentage', 'party')
    return render(request, 'legislator/index/index_ordered.html', {'ad': ad, 'ly_list': ly_list, 'outof_ly_list': outof_ly_list, 'param': maps[index], 'index': index})

def counties(request, ad):
    ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=True)\
                                      .order_by('-county', 'party')
    outof_ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=False)
    return render(request, 'legislator/index/countys.html', {'ad': ad, 'ly_list': ly_list, 'outof_ly_list': outof_ly_list})

def county(request, county, ad):
    ly_list = LegislatorDetail.objects.filter(ad=ad, in_office=True, county=county)\
                                      .order_by('party', 'name')
    return render(request, 'legislator/county.html', {'ad': int(ad), 'ly_list': ly_list, 'county': county})

def committee(request, committee, ad):
    ly_list = Legislator_Committees.objects.select_related('legislator').filter(ad=ad, legislator__in_office=True, committee=committee).order_by('-session', 'legislator__party', 'legislator__name')
    return render(request, 'legislator/committee.html',  {'ly_list': ly_list, 'committee': committee})

def personal_political_contributions(request, legislator_id, ad):
    ly = get_object_or_404(LegislatorDetail.objects, ad=ad, legislator_id=legislator_id)
    try:
        pc = ly.elected_candidate.get().politicalcontributions
        return render(request, 'legislator/personal_politicalcontributions.html', {'ly': ly, 'pc': pc})
    except Exception, e:
        raise Http404

def voter_standpoints(request, legislator_id, ad):
    ly = get_object_or_404(LegislatorDetail.objects, ad=ad, legislator_id=legislator_id)
    c = connections['default'].cursor()
    qs = u'''
        SELECT
        CASE
            WHEN lv.decision = 1 THEN '贊成'
            WHEN lv.decision = -1 THEN '反對'
            WHEN lv.decision = 0 THEN '棄權'
            WHEN lv.decision isnull THEN '沒投票'
            END as decision,
            s.title,
            count(*) as times,
            json_agg(v) as votes
        FROM vote_legislator_vote lv
        JOIN standpoint_standpoint s on s.vote_id = lv.vote_id
        JOIN vote_vote v on lv.vote_id = v.uid
        WHERE
    '''
    if request.GET.get('keyword'):
        qs = qs + 's.title = %s AND'
        param = [request.GET['keyword'], ly.id]
    else:
        param = [ly.id]
    qs = qs + '''
            lv.legislator_id = %s AND s.pro = (
                SELECT max(pro)
                FROM standpoint_standpoint ss
                WHERE ss.pro > 0 AND s.vote_id = ss.vote_id
                GROUP BY ss.vote_id
            )
        GROUP BY s.title, lv.decision
        ORDER BY times DESC
    '''
    c.execute(qs, param)
    standpoints = [
        dict(zip([col[0] for col in c.description], row))
        for row in c.fetchall()
    ]
    keyword_obj = list(Standpoint.objects.filter(pro__gt=0).values_list('title', flat=True).distinct())
    return render(request, 'legislator/voter_standpoints.html', {'ly': ly, 'standpoints': standpoints, 'keyword_obj': keyword_obj})

def voter_detail(request, legislator_id, ad):
    ly = get_object_or_404(LegislatorDetail.objects, ad=ad, legislator_id=legislator_id)
    qs = Q(conflict=True) if request.GET.get('conscience') else Q()
    if request.GET.get('decision'):
        decisions = {"agree": Q(decision=1), "disagree": Q(decision=-1), "abstain": Q(decision=0), "notvote": Q(decision__isnull=True)}
        qs = qs & decisions.get(request.GET['decision'], Q())
    hsqs = Q(tags_num__gt=0) if request.GET.get('has_tag') else Q()
    hsqs = hsqs & Q(content=request.GET['keyword']) if request.GET.get('keyword') else hsqs
    if hsqs != Q():
        sqs = SearchQuerySet().filter(hsqs).models(Vote)
        votes = ly.votes.select_related('vote', 'vote__sitting').filter(qs & Q(vote_id__in=[x.uid for x in sqs]))
    else:
        votes = ly.votes.select_related('vote', 'vote__sitting').filter(qs)
    keywords = [x.content for x in SearchQuerySet().filter(category__exact=2).models(Keyword).order_by('-hits')]
    return render(request, 'legislator/voter_detail.html', {'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'ly': ly, 'origin': qs & hsqs == Q(), 'votes': votes, 'keyword': request.GET.get('keyword', '')})

def biller_detail(request, legislator_id, ad):
    ly = get_object_or_404(LegislatorDetail.objects, ad=ad, legislator_id=legislator_id)
    bills = ly.bills.filter(legislator_id=ly.id, priproposer=True)
    qs = Q(uid__in=bills.values_list('bill_id', flat=True))
    qs = qs & Q(content=request.GET['keyword']) if request.GET.get('keyword') else qs
    bills = SearchQuerySet().filter(qs).models(Bill).order_by('-last_action_at')
    keywords = keyword_list(3)
    return render(request, 'legislator/biller_detail.html',  {'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'bills': bills, 'ly': ly, 'keyword': request.GET.get('keyword', '')})

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
    ly_obj, legend = [], []
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
            "column": 'vote_param',
            "key": 'conflict',
        },
        "vote": {
            "legend": u'表決缺席次數',
            "column": 'vote_param',
            "key": 'not_voting',
        },
        "biller": {
            "legend": u'法條修正草案數',
            "column": 'bill_param',
            "key": 'chief',
        }
    }
    filter_dict = {
        "ad": 8,
        "party": party,
        "elected_candidate__politicalcontributions__isnull": False
    }
    if pc_field.get(index) and index_field.get(compare):
        legend = [pc_field[index], index_field[compare].get('legend'), 'money', 'count']
        ly_obj = LegislatorDetail.objects.filter(**filter_dict)\
                                         .extra(select={
                                             'totalNum': "SELECT cast(COALESCE(politicalcontributions::json->'in'->>'%s', politicalcontributions::json->'out'->>'%s', politicalcontributions::json->>'%s') as int) FROM candidates_candidates WHERE candidates_candidates.legislator_id = legislator_legislatordetail.id" % (index, index, index),
                                             'compare': "SELECT cast(%s::json->>'%s' as int) FROM candidates_candidates WHERE candidates_candidates.legislator_id = legislator_legislatordetail.id" % (index_field[compare]['column'], index_field[compare]['key']),
                                         },)\
                                         .order_by('-totalNum')
    elif pc_field.get(index) and pc_field.get(compare):
        legend = [pc_field[index], pc_field[compare], 'money', 'money']
        ly_obj = LegislatorDetail.objects.filter(**filter_dict)\
                                         .extra(select={
                                             'totalNum': "SELECT cast(COALESCE(politicalcontributions::json->'in'->>'%s', politicalcontributions::json->'out'->>'%s', politicalcontributions::json->>'%s') as int) FROM candidates_candidates WHERE candidates_candidates.legislator_id = legislator_legislatordetail.id" % (index, index, index),
                                             'compare': "SELECT cast(COALESCE(politicalcontributions::json->'in'->>'%s', politicalcontributions::json->'out'->>'%s', politicalcontributions::json->>'%s') as int) FROM candidates_candidates WHERE candidates_candidates.legislator_id = legislator_legislatordetail.id" % (compare, compare, compare),
                                         },)\
                                         .order_by('-totalNum')
    else:
        raise Http404
    return render(request, 'legislator/chart_report_for_political_contribution.html',  {'compare': compare, 'legend': legend, 'party': party, 'index': index, 'ly_name':  [ly.name for ly in ly_obj], 'ly_obj': ly_obj, 'data': list(ly_obj.values('name',  'totalNum',  'compare')), 'pc_field': sorted(pc_field.items()), 'index_field': index_field})
