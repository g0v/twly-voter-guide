# -*- coding: utf-8 -*-
import operator
import re
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F, Q
from .models import Legislator, LegislatorDetail, Platform, Attendance, PoliticalContributions
from vote.models import Vote, Legislator_Vote
from proposal.models import Proposal
from bill.models import Bill
from sittings.models import Sittings
from committees.models import Committees, Legislator_Committees
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def get_legislator(legislator_id):
    try:
        ly = LegislatorDetail.objects.get(ad=8, legislator_id=legislator_id)
        if ly:
            ly.hits = F('hits') + 1
            ly.save(update_fields=['hits'])
        return ly
    except Exception, e:
        print e

def index(request, index):
    error, proposertype, progress, query = None, False, "", Q(ad=8, in_office=True)
    outof_ly_list = LegislatorDetail.objects.filter(ad=8, in_office=False)
    if 'lyname' in request.GET:
        ly_name = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['lyname']).strip()
        if ly_name:
            query = query & Q(name__icontains=ly_name)
        else:
            error = True
    name_query = query
    if index == 'biller':
        query = query & Q(legislator_bill__petition=False) # don't include petition legislators
        if 'proposertype' in request.GET:
            proposertype = request.GET['proposertype']
            if not proposertype: # only primary_proposer count
                query = query & Q(legislator_bill__priproposer=True)
        else: # no form submit
            query = query & Q(legislator_bill__priproposer=True)
        if 'progress' in request.GET:
            progress = request.GET['progress']
            if progress:
                query = query & Q(legislator_bill__bill__last_action=progress)
        ly_list = LegislatorDetail.objects.filter(query).annotate(totalNum=Count('legislator_bill__id')).exclude(totalNum=0).order_by('-totalNum')
        no_count_list = LegislatorDetail.objects.filter(name_query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True))
        return render(request,'legislator/index/index_ordered.html', {'no_count_list':no_count_list,'proposertype':proposertype,'progress':progress,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    elif index == 'conscience_vote':
        ly_list = LegislatorDetail.objects.filter(query, votes__conflict=True).annotate(totalNum=Count('votes__id')).order_by('-totalNum','party')
        no_count_list = LegislatorDetail.objects.filter(name_query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True)).order_by('party')
        return render(request,'legislator/index/index_ordered.html', {'no_count_list':no_count_list,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    elif index == 'notvote':
        ly_list = LegislatorDetail.objects.filter(query, votes__decision__isnull=True).annotate(totalNum=Count('votes__id')).order_by('-totalNum','party')
        no_count_list = LegislatorDetail.objects.filter(name_query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True))
        return render(request,'legislator/index/index_ordered.html', {'no_count_list':no_count_list,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    elif index == 'committee':
        ly_list = Legislator_Committees.objects.select_related().filter(ad=8).order_by('committee', 'session', 'legislator__party', 'legislator__name')
        return render(request,'legislator/index/committees.html', {'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    elif index == 'district':
        ly_list = LegislatorDetail.objects.filter(query).order_by('-county','party')
        return render(request,'legislator/index/countys.html', {'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    else:
        return HttpResponseRedirect('/legislator/biller')

def index_district(request, index):
    ly_list = LegislatorDetail.objects.filter(ad=8, in_office=True, county=index).order_by('party', 'name')
    return render(request,'legislator/county.html', {'ly_list': ly_list,'index':index})

def index_committee(request, index):
    ly_list = Legislator_Committees.objects.select_related().filter(ad=8, committee=index).order_by('-session', 'legislator__party', 'legislator__name')
    return render(request,'legislator/committee.html', {'ly_list': ly_list,'index':index})

def proposer_detail(request, legislator_id, keyword_url):
    proposertype = False
    ly = get_legislator(legislator_id)
    if not ly:
        return HttpResponseRedirect('/')
    query = Q(proposer__id=ly.id, legislator_proposal__priproposer=True)
    if 'proposertype' in request.GET:
        proposertype = request.GET['proposertype']
        if proposertype:
            query = Q(proposer__id=ly.id)
    keyword = keyword_normalize(request, keyword_url)
    if keyword:
        proposal = Proposal.objects.filter(query & reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-sitting__date')
        if proposal:
            keyword_been_searched(keyword, 1)
    else:
        proposal = Proposal.objects.filter(query).order_by('-sitting__date')
    return render(request,'legislator/proposer_detail.html', {'keyword_obj':keyword_list(1),'proposal':proposal,'ly':ly,'keyword':keyword,'proposertype':proposertype})

def voter_detail(request, legislator_id, index, keyword_url):
    votes, notvote, query = None, False, Q()
    ly = get_legislator(legislator_id)
    if not ly:
        return HttpResponseRedirect('/')
    #--> 沒投票的表決是否搜尋
    if 'notvote' in request.GET:
        notvote = request.GET['notvote']
        if notvote:
            query = Q(decision__isnull=False)
    #<--
    # 脫黨投票
    if index == 'conscience':
        query = query & Q(legislator_id=ly.id, conflict=True)
    else:
        query = query & Q(legislator_id=ly.id)
    #<--
    keyword = keyword_normalize(request, keyword_url)
    if keyword:
        votes = Legislator_Vote.objects.select_related().filter(query & reduce(operator.and_, (Q(vote__content__icontains=x) for x in keyword.split()))).order_by('-vote__sitting__date')
        if votes:
            keyword_been_searched(keyword, 2)
    else:
        votes = Legislator_Vote.objects.select_related().filter(query).order_by('-vote__sitting__date')
    vote_addup = votes.values('decision').annotate(totalNum=Count('vote', distinct=True)).order_by('-decision')
    return render(request,'legislator/voter_detail.html', {'keyword_obj':keyword_list(2),'ly':ly,'index':index,'votes':votes,'keyword':keyword,'vote_addup':vote_addup,'notvote':notvote})

def biller_detail(request, legislator_id, keyword_url):
    proposertype = False
    ly = get_legislator(legislator_id)
    if not ly:
        return HttpResponseRedirect('/')
    query = Q(proposer__id=ly.id, legislator_bill__priproposer=True)
    if 'proposertype' in request.GET:
        proposertype = request.GET['proposertype']
        if proposertype:
            query = Q(proposer__id=ly.id)
    bills = Bill.objects.filter(query)
    keyword = keyword_normalize(request, keyword_url)
    if keyword:
        bills = bills.filter(query & reduce(operator.and_, (Q(abstract__icontains=x) for x in keyword.split())))
        if bills:
            keyword_been_searched(keyword, 3)
    else:
        bills = bills.filter(query)
    return render(request,'legislator/biller_detail.html', {'keyword_obj':keyword_list(3),'bills':bills,'ly':ly,'keyword':keyword,'proposertype':proposertype})

def platformer_detail(request, legislator_id):
    ly = get_legislator(legislator_id)
    if not ly:
        return HttpResponseRedirect('/')
    if ly.constituency == u'全國不分區':
        politics = Platform.objects.filter(party=ly.party).order_by('id')
    else:
        politics = Platform.objects.filter(legislator_id=ly.id).order_by('id')
    return render(request,'legislator/ly_politics.html', {'ly':ly,'politics':politics})

def chart_report(request, index='vote'):
    ly_obj, ly_name, vote_obj, title, content, compare, data = [], [], [], None, None, None, None
    if index == 'vote':
        compare = Vote.objects.count()
        ly_obj = LegislatorDetail.objects.filter(in_office=True, votes__decision__isnull=True).annotate(totalNum=Count('votes__id')).order_by('-totalNum','party')[:10]
        title, content = u'立法院表決缺席前十名', u'可和立法院開會缺席交叉比較，為何開會有出席但沒有參加表決？(點選立委名字可看立委個人投票紀錄)'
    elif index == 'conscience_vote':
        compare = Vote.objects.count()
        ly_obj = LegislatorDetail.objects.filter(in_office=True, votes__conflict=True).annotate(totalNum=Count('votes__id')).order_by('-totalNum','party')[:10]
        title, content = u'脫黨投票次數前十名', u'脫黨投票不一定較好，可能該立委是憑良心投票，也可能是受財團、企業影響所致，還請點選該立委觀看其脫黨投票的表決內容再作論定。'
    elif index == 'attend_committee':
        compare = "{0:.2f}".format(Attendance.objects.filter(category='committee', status='attend').count()/116.0)
        ly_obj = LegislatorDetail.objects.filter(in_office=True, attendance__category='committee', attendance__status='attend').annotate(totalNum=Count('attendance__id')).order_by('-totalNum','party')[:10]
        title, content = u'委員會開會列席(旁聽)次數前十名', u'委員非該委員會仍列席參加的次數排行(量化數據不能代表好壞只能參考)'
    elif index == 'biller':
        compare = "{0:.2f}".format(Bill.objects.count()/116.0)
        ly_obj = LegislatorDetail.objects.filter(in_office=True, legislator_bill__priproposer=True, legislator_bill__petition=False).annotate(totalNum=Count('legislator_bill__id')).order_by('-totalNum','party')[:10]
        title, content = u'法條修正草案數前十名', u'量化數據不能代表好壞只能參考，修正草案數多不一定較好，還請點選該立委觀看其修正草案的內容再作論定。'
    elif index == 'proposal':
        compare = "{0:.2f}".format(Proposal.objects.count()/116.0)
        ly_obj = LegislatorDetail.objects.filter(in_office=True, legislator_proposal__priproposer=True).annotate(totalNum=Count('legislator_proposal__id')).order_by('-totalNum','party')[:10]
        title, content = u'附帶決議、臨時提案數前十名', u'量化數據不能代表好壞只能參考，提案數多不一定較好，還請點選該立委觀看其提案的內容再作論定。'
    elif index == 'committee':
        ly_obj = LegislatorDetail.objects.filter(in_office=True, attendance__category='committee', attendance__status='absent').annotate(totalNum=Count('attendance__id')).order_by('-totalNum','party')[:10]
        title, content = u'委員會開會缺席前十名', u'委員會是法案推行的第一關卡，立委需在委員會提出法案的增修(點選立委名字可看立委個人提案)'
    elif index == 'ly':
        compare = Sittings.objects.filter(committee='').count()
        ly_obj = LegislatorDetail.objects.filter(in_office=True, attendance__category='YS', attendance__status='absent').annotate(totalNum=Count('attendance__id')).order_by('-totalNum','party')[:10]
        title, content = u'立法院開會缺席前十名', u'立委須參加立法院例行會議，在會議中進行質詢、法案討論表決、人事表決等重要工作(點選立委名字可看立委投票紀錄)'
    return render(request,'legislator/chart_report.html', {'compare':compare,'title':title,'content':content,'index':index,'vote_obj':vote_obj,'ly_name': [ly.name for ly in ly_obj],'ly_obj':ly_obj, 'data': list(ly_obj.values('name', 'totalNum'))} )

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
        "proposal": {
            "legend": u'附帶決議、臨時提案數',
            "query": 'SELECT COUNT(*) FROM proposal_legislator_proposal WHERE proposal_legislator_proposal.priproposer=True AND proposal_legislator_proposal.legislator_id = legislator_legislatordetail.id GROUP BY proposal_legislator_proposal.legislator_id'
        },
        "biller": {
            "legend": u'法條修正草案數',
            "query": 'SELECT COUNT(*) FROM bill_legislator_bill WHERE bill_legislator_bill.priproposer=True AND bill_legislator_bill.petition=False AND bill_legislator_bill.legislator_id = legislator_legislatordetail.id GROUP BY bill_legislator_bill.legislator_id'
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

'''
def list_union(month_list, obj_q):
    obj = []
    for e in month_list:
        match = False
        for q in obj_q:
            if e.year == q['year'] and e.month == q['month']:
                obj.append({'year':e.year,'month':e.month,'n':q['id__count']})
                match = True
                break
        if not match:
            obj.append({'year':e.year,'month':e.month,'n':0})
    return obj

def chart_personal_report(request, legislator_id, index='proposal'):
    ly = LegislatorDetail.objects.get(ad=8, legislator_id=legislator_id)
    if index == 'proposal':
        query_p = Q(date__gte=ly.term_start,legislator_proposal__priproposer=True)
        compare_obj = Proposal.objects.filter(query_p & Q(proposer__in_office=True)).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Proposal.objects.filter(query_p & Q(proposer__id=ly.id)).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Proposal.objects.filter(date__gte=ly.term_start).dates('date','month')
        obj = list_union(month_list, obj_q)
    elif index == 'vote':
        compare_obj = Vote.objects.filter(date__gte=ly.term_start).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Vote.objects.filter(date__gte=ly.term_start, voter__id=ly.id, legislator_vote__decision__isnull=False).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Vote.objects.filter(date__gte=ly.term_start).dates('date','month')
        obj = list_union(month_list, obj_q)
    elif index == 'ly':
        compare_obj = Attendance.objects.filter(legislator_id=ly.id, category='YS').extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Attendance.objects.filter(legislator_id=ly.id, category='YS', status='present').extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Attendance.objects.filter(date__gte=ly.term_start, category='YS').dates('date','month')
        obj = list_union(month_list, obj_q)
    return render(request,'legislator/chart_personal_report.html', {'index':index,'ly':ly,'obj':obj,'compare_obj':compare_obj} )
'''
