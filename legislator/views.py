# -*- coding: utf-8 -*-
import operator
import re
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F, Q
from .models import Legislator, LegislatorDetail, Platform, Attendance
from vote.models import Vote,Legislator_Vote
from proposal.models import Proposal
from bill.models import Bill
from search.models import Keyword
from sittings.models import Sittings
from committees.models import Committees, Legislator_Committees
from search.views import keyword_list


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
                print(progress)
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
    return render(request,'legislator/county.html', {'ly_list': ly_list,'type':'district','index':index})

def index_committee(request, index):
    ly_list = Legislator_Committees.objects.select_related().filter(ad=8, committee=index).order_by('-session', 'legislator__party', 'legislator__name')
    return render(request,'legislator/committee.html', {'ly_list': ly_list,'index':index})

def proposer_detail(request, legislator_id, keyword_url):
    error,keyword,proposertype = False,None,False
    ly = get_legislator(legislator_id)
    if not ly:
        return HttpResponseRedirect('/')
    query = Q(proposer__id=ly.id, legislator_proposal__priproposer=True)
    if 'proposertype' in request.GET:
        proposertype = request.GET['proposertype']
        if proposertype:
            query = Q(proposer__id=ly.id)
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        proposal = Proposal.objects.filter(query & reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-sitting__date')
        if proposal:
            proposal.filter(hits__isnull=False).update(hits=F('hits')+1)
            proposal.filter(hits__isnull=True).update(hits=1)
            keyword_obj = Keyword.objects.filter(category=1, content=keyword.strip())
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            else:
                k = Keyword(content=keyword.strip(), category=1, valid=True, hits=1)
                k.save()
    else:
        proposal = Proposal.objects.filter(query).order_by('-sitting__date')
    return render(request,'legislator/proposer_detail.html', {'keyword_obj':keyword_list(1),'proposal':proposal,'ly':ly,'keyword':keyword,'error':error,'proposertype':proposertype})

def voter_detail(request, legislator_id, index, keyword_url):
    keyword, keyword_valid, votes, error, notvote, query = None, False, None, False, False, Q()
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
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        keyword_valid = True
        votes = Legislator_Vote.objects.select_related().filter(query & reduce(operator.and_, (Q(vote__content__icontains=x) for x in keyword.split()))).order_by('-vote')
        if votes:
            keyword_obj = Keyword.objects.filter(category=2, content=keyword.strip())
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            else:
                k = Keyword(content=keyword.strip(), category=2, valid=True, hits=1)
                k.save()
    else:
        votes = Legislator_Vote.objects.select_related().filter(query).order_by('-vote')
    vote_addup = votes.values('decision').annotate(totalNum=Count('vote', distinct=True)).order_by('-decision')
    return render(request,'legislator/voter_detail.html', {'keyword_obj':keyword_list(2),'ly':ly,'index':index,'votes':votes,'keyword':keyword,'error':error,'vote_addup':vote_addup,'notvote':notvote})

def biller_detail(request, legislator_id, keyword_url):
    law, error, keyword, proposertype = None, False, None, False
    ly = get_legislator(legislator_id)
    if not ly:
        return HttpResponseRedirect('/')
    query = Q(proposer__id=ly.id, legislator_bill__priproposer=True)
    if 'proposertype' in request.GET:
        proposertype = request.GET['proposertype']
        if proposertype:
            query = Q(proposer__id=ly.id)
    bills = Bill.objects.filter(query)
    #laws = bills.values('law').distinct().order_by('law')
    #if 'law' in request.GET:
    #    law = request.GET['law']
    #    if law:
    #        query = query & Q(law=law)
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        bills = bills.filter(query & reduce(operator.or_, (Q(abstract__icontains=x) for x in keyword.split())))
    else:
        bills = bills.filter(query)
    return render(request,'legislator/biller_detail.html', {'keyword_obj':keyword_list(3),'bills':bills,'ly':ly,'keyword':keyword,'error':error,'proposertype':proposertype})

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
    ly_obj, ly_name, vote_obj,title,content,compare, data = [], [], [], None, None, None, None
    if index == 'vote':
        compare = Vote.objects.count()
        ly_obj = LegislatorDetail.objects.filter(in_office=True, votes__decision__isnull=True).annotate(totalNum=Count('votes__id')).order_by('-totalNum','party')[:10]
        data = list(ly_obj.values('name', 'totalNum'))
        title, content = u'立法院表決缺席前十名', u'可和立法院開會缺席交叉比較，為何開會有出席但沒有參加表決？(點選立委名字可看立委個人投票紀錄)'
    elif index == 'conscience_vote':
        compare = Vote.objects.count()
        ly_obj = LegislatorDetail.objects.filter(in_office=True, votes__conflict=True).annotate(totalNum=Count('votes__id')).order_by('-totalNum','party')[:10]
        data = list(ly_obj.values('name', 'totalNum'))
        title, content = u'脫黨投票次數前十名', u'脫黨投票不一定較好，可能該立委是憑良心投票，也可能是受財團、企業影響所致，還請點選該立委觀看其脫黨投票的表決內容再作論定。'
    elif index == 'attend_committee':
        compare = "{0:.2f}".format(Attendance.objects.filter(category='committee', status='attend').count()/116.0)
        ly_obj = LegislatorDetail.objects.filter(in_office=True, attendance__category='committee', attendance__status='attend').annotate(totalNum=Count('attendance__id')).order_by('-totalNum','party')[:10]
        data = list(ly_obj.values('name', 'totalNum'))
        title, content = u'委員會開會列席(旁聽)次數前十名', u'委員非該委員會仍列席參加的次數排行(量化數據不能代表好壞只能參考)'
    elif index == 'biller':
        compare = "{0:.2f}".format(Bill.objects.count()/116.0)
        ly_obj = LegislatorDetail.objects.filter(in_office=True, legislator_bill__priproposer=True, legislator_bill__petition=False).annotate(totalNum=Count('legislator_bill__id')).order_by('-totalNum','party')[:10]
        data = list(ly_obj.values('name', 'totalNum'))
        title, content = u'法條修正草案數前十名', u'量化數據不能代表好壞只能參考，修正草案數多不一定較好，還請點選該立委觀看其修正草案的內容再作論定。'
    elif index == 'proposal':
        compare = "{0:.2f}".format(Proposal.objects.count()/116.0)
        ly_obj = LegislatorDetail.objects.filter(in_office=True, legislator_proposal__priproposer=True).annotate(totalNum=Count('legislator_proposal__id')).order_by('-totalNum','party')[:10]
        data = list(ly_obj.values('name', 'totalNum'))
        title, content = u'附帶決議、臨時提案數前十名', u'量化數據不能代表好壞只能參考，提案數多不一定較好，還請點選該立委觀看其提案的內容再作論定。'
    elif index == 'committee':
        ly_obj = LegislatorDetail.objects.filter(in_office=True, attendance__category='committee', attendance__status='absent').annotate(totalNum=Count('attendance__id')).order_by('-totalNum','party')[:10]
        data = list(ly_obj.values('name', 'totalNum'))
        title, content = u'委員會開會缺席前十名', u'委員會是法案推行的第一關卡，立委需在委員會提出法案的增修(點選立委名字可看立委個人提案)'
    elif index == 'ly':
        compare = Sittings.objects.filter(committee='').count()
        ly_obj = LegislatorDetail.objects.filter(in_office=True, attendance__category='YS', attendance__status='absent').annotate(totalNum=Count('attendance__id')).order_by('-totalNum','party')[:10]
        data = list(ly_obj.values('name', 'totalNum'))
        title, content = u'立法院開會缺席前十名', u'立委須參加立法院例行會議，在會議中進行質詢、法案討論表決、人事表決等重要工作(點選立委名字可看立委投票紀錄)'
    elif index == 'nvote_gbdate':
        vote_obj = Vote.objects.values('sitting__date','sitting__name').annotate(totalNum=Count('id', distinct=True)).order_by('sitting__date')
        title = u'立法院表決數依日期分組'
    elif index == 'nvote_gbmonth':
        vote_obj = Vote.objects.extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(totalNum=Count('id', distinct=True)).order_by('year','month')
        title = u'立法院表決數依月份分組'
    return render(request,'legislator/chart_report.html', {'compare':compare,'title':title,'content':content,'index':index,'vote_obj':vote_obj,'ly_name': [ly.name for ly in ly_obj],'ly_obj':ly_obj, 'data': data} )

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
