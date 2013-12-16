# -*- coding: utf-8 -*-
import operator,re
from itertools import chain
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.db.models import Count,Sum,F,Q
from legislator.models import Legislator,LegislatorDetail,Politics,Attendance
from vote.models import Vote,Legislator_Vote
from proposal.models import Proposal
from bill.models import Bill
from search.models import Keyword
from search.views import keyword_list


def index(request,index):
    error, proposertype, query = None, False, Q(ad=8, in_office=True)
    outof_ly_list = LegislatorDetail.objects.filter(ad=8, in_office=False)
    if 'lyname' in request.GET:
        ly_name = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['lyname']).strip()
        if ly_name:
            query = query & Q(name__icontains=ly_name)
        else:
            error = True
    name_query = query
    if index == 'biller':
        if 'proposertype' in request.GET:
            proposertype = request.GET['proposertype']
            if not proposertype:
                query = query & Q(legislator__legislator_bill__priproposer=True)
                no_count_list = LegislatorDetail.objects.filter(name_query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True))
        else:
            query = query & Q(legislator__legislator_bill__priproposer=True)
        ly_list = LegislatorDetail.objects.filter(query).annotate(totalNum=Count('legislator__legislator_bill__id')).exclude(totalNum=0).order_by('-totalNum')
        no_count_list = LegislatorDetail.objects.filter(name_query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True))
        return render(request,'legislator/index/index_ordered.html', {'no_count_list':no_count_list,'proposertype':proposertype,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    elif index == 'conscience_vote':
        ly_list = LegislatorDetail.objects.filter(query,legislator__legislator_vote__conflict=True).annotate(totalNum=Count('legislator__legislator_vote__id')).order_by('-totalNum','party')
        no_count_list = LegislatorDetail.objects.filter(name_query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True)).order_by('party')
        return render(request,'legislator/index/index_ordered.html', {'no_count_list':no_count_list,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    elif index == 'notvote':
        ly_list = LegislatorDetail.objects.filter(query,legislator__legislator_vote__decision__isnull=True).annotate(totalNum=Count('legislator__legislator_vote__id')).order_by('-totalNum','party')
        no_count_list = LegislatorDetail.objects.filter(name_query).exclude(legislator_id__in=ly_list.values_list('legislator_id', flat=True))
        return render(request,'legislator/index/index_ordered.html', {'no_count_list':no_count_list,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    elif index == 'committee':
        ly_list = LegislatorDetail.objects.filter(query).order_by('committee','party')
        return render(request,'legislator/index/index_committee.html', {'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    elif index == 'district':
        ly_list = Legislator.objects.filter(query).order_by('district','party')
        return render(request,'legislator/index/index_district.html', {'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error})
    else:
        return HttpResponseRedirect('/legislator/biller/')

def index_district(request,index):
    ly_list = Legislator.objects.filter(in_office=True,district=index).order_by('eleDistrict')
    return render(request,'legislator/index_filter.html', {'ly_list': ly_list,'type':'district','index':index})

def index_committee(request,index):
    ly_list = LegislatorDetail.objects.filter(in_office=True,committee=index).order_by('district')
    return render(request,'legislator/index_filter.html', {'ly_list': ly_list,'type':'committee','index':index})

def proposer_detail(request,legislator_id,keyword_url):
    error,keyword,proposertype = False,None,False
    ly = get_object_or_404(Legislator, pk=legislator_id)
    if ly:
        if ly.hits:
            ly.hits = F('hits') + 1
        else:
            ly.hits = 1
        ly.save(update_fields=['hits'])
    query = Q(proposer__id=legislator_id,legislator_proposal__priproposer=True)
    if 'proposertype' in request.GET:
        proposertype = request.GET['proposertype']
        if proposertype:
            query = Q(proposer__id=legislator_id)
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        proposal = Proposal.objects.filter(query & reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-date').defer('sessionPrd','session')
        if proposal:
            proposal.filter(hits__isnull=False).update(hits=F('hits')+1)
            proposal.filter(hits__isnull=True).update(hits=1)
            keyword_obj = Keyword.objects.filter(category=1,content=keyword.strip())
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            else:
                k = Keyword(content=keyword.strip(),category=1,valid=True,hits=1)
                k.save()
    else:
        proposal = Proposal.objects.filter(query).order_by('-date').defer('sessionPrd','session')
    return render(request,'legislator/proposer_detail.html', {'keyword_obj':keyword_list(1),'proposal':proposal,'ly':ly,'keyword':keyword,'error':error,'proposertype':proposertype})

def voter_detail(request,legislator_id,index,keyword_url):
    keyword,keyword_valid,votes,error,notvote,notvote_votelist = None,False,None,False,False,None
    ly = Legislator.objects.get(pk=legislator_id)
    if ly:
        if ly.hits:
            ly.hits = F('hits') + 1
        else:
            ly.hits = 1
        ly.save(update_fields=['hits'])
    if index == 'conscience':
        query = Q(legislator_id=legislator_id,conflict=True)
    else:
        query = Q(legislator_id=legislator_id)
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        keyword_valid = True
        votes = Legislator_Vote.objects.select_related().filter(query & reduce(operator.and_, (Q(vote__content__icontains=x) for x in keyword.split()))).order_by('-vote__date','-pk')
        if votes:
            keyword_obj = Keyword.objects.filter(category=2,content=keyword.strip())
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            else:
                k = Keyword(content=keyword.strip(),category=2,valid=True,hits=1)
                k.save()
    else:
        votes = Legislator_Vote.objects.select_related().filter(query).order_by('-vote__date','-pk')
    if 'notvote' in request.GET:
        notvote = request.GET['notvote']
        if notvote:
            if not keyword_valid:
                notvote_votelist = Vote.objects.exclude(id__in = votes.values_list('vote_id', flat=True)).order_by('-date','-pk')
            else:
                notvote_votelist = Vote.objects.exclude(id__in = votes.values_list('vote_id', flat=True)).filter(reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-date','-pk')
    vote_addup = votes.values('decision').annotate(totalNum=Count('vote', distinct=True)).order_by('-decision')
    return render(request,'legislator/voter_detail.html', {'keyword_obj':keyword_list(2),'ly':ly,'index':index,'votes':votes,'keyword':keyword,'error':error,'vote_addup':vote_addup,'notvote':notvote,'notvote_votelist':notvote_votelist})

def ly_politics(request, legislator_id):
    ly = Legislator.objects.get(pk=legislator_id)
    if ly.eleDistrict == u'全國不分區':
        politics = Politics.objects.filter(party=ly.party).order_by('id')
    else:
        politics = Politics.objects.filter(legislator_id=legislator_id).order_by('id')
    return render(request,'legislator/ly_politics.html', {'ly':ly,'politics':politics})

def chart_report(request,index='ly_hit'):
    ly_obj, ly_name, vote_obj,title,content,compare = [], [], [], None, None, None
    if index == 'vote':
        compare = Vote.objects.count()
        ly_obj = LegislatorDetail.objects.filter(in_office=True,legislator__legislator_vote__decision__isnull=True).annotate(totalNum=Count('legislator__legislator_vote__id')).order_by('-totalNum','party')[:10]
        chart_data = [ly.totalNum for ly in ly_obj]
        title, content = u'立法院表決缺席前十名', u'每一次會議的最後會進行表決，可和立法院開會缺席交叉比較，為何開會有出席但沒有參加表決？(點選立委名字可看立委個人圖表)'
    elif index == 'conscience_vote':
        compare = Vote.objects.count()
        ly_obj = LegislatorDetail.objects.filter(in_office=True,legislator__legislator_vote__conflict=True).annotate(totalNum=Count('legislator__legislator_vote__id')).order_by('-totalNum','party')[:10]
        chart_data = [ly.totalNum for ly in ly_obj]
        title, content = u'脫黨投票次數前十名', u'點選立委名字可看立委脫黨投票的表決內容'
    elif index == 'biller':
        compare = "{0:.2f}".format(Bill.objects.count()/113.0)
        ly_obj = Legislator.objects.filter(in_office=True,legislator_bill__priproposer=True).annotate(totalNum=Count('legislator_bill__id')).order_by('-totalNum','party')[:10]
        chart_data = [ly.totalNum for ly in ly_obj]
        title, content = u'法條修正草案數前十名', u'立委在委員會中通過的法條修正草案數(點選立委名字可看立委個人提出的法案條修正草案)'
    elif index == 'proposal':
        compare = "{0:.2f}".format(Proposal.objects.count()/113.0)
        ly_obj = Legislator.objects.filter(in_office=True,legislator_proposal__priproposer=True).annotate(totalNum=Count('legislator_proposal__id')).order_by('-totalNum','party')[:10]
        chart_data = [ly.totalNum for ly in ly_obj]
        title, content = u'附帶決議、臨時提案數前十名', u'立委在委員會中提出的法案數，此處只有主提案人才會記數(點選立委名字可看立委個人圖表)'
    elif index == 'committee':
        ly_obj = Legislator.objects.filter(in_office=True,attendance__category=1).annotate(totalNum=Sum('attendance__unpresentNum')).order_by('-totalNum','party')[:10]
        chart_data = [ly.totalNum for ly in ly_obj]
        title, content = u'委員會開會缺席前十名', u'委員會是法案推行的第一關卡，立委需在委員會提出法案的增修(點選立委名字可看立委個人圖表)'
    elif index == 'ly':
        compare = Attendance.objects.values('session').filter(category=0).distinct().count()
        ly_obj = Legislator.objects.filter(in_office=True,attendance__category=0).annotate(totalNum=Sum('attendance__unpresentNum')).order_by('-totalNum','party')[:10]
        chart_data = [ly.totalNum for ly in ly_obj]
        title, content = u'立法院開會缺席前十名', u'立委須參加立法院例行會議，在會議中進行質詢、法案討論表決、人事表決等重要工作(點選立委名字可看立委個人圖表)'
    elif index == 'ly_hit':
        ly_obj = Legislator.objects.filter(in_office=True,hits__isnull=False).order_by('-hits','party')[:10]
        chart_data = [ly.hits for ly in ly_obj]
        title, content = u'點閱次數前十名', u'各立委在本站點閱次數排行'
    elif index == 'nvote_gbdate':
        vote_obj = Vote.objects.values('date','session').annotate(totalNum=Count('id', distinct=True)).order_by('date')
        title = u'立法院表決數依日期分組'
    elif index == 'nvote_gbmonth':
        vote_obj = Vote.objects.extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(totalNum=Count('id', distinct=True)).order_by('year','month')
        title = u'立法院表決數依月份分組'
    else:
        ly_obj = Legislator.objects.filter(in_office=True,hits__isnull=False).order_by('-hits')[:10]
        ly_name = ly_obj.values_list('name', flat=True)
        title, content = u'立委點閱次數前十名', u'各立委在本站點閱次數排行'
    return render(request,'legislator/chart_report.html', {'compare':compare,'title':title,'content':content,'index':index,'vote_obj':vote_obj,'ly_name': [ly.name for ly in ly_obj],'ly_obj':ly_obj, 'chart_data':chart_data} )

def list_union(month_list,obj_q):
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

def chart_personal_report(request,legislator_id,index='proposal'):
    ly = Legislator.objects.get(pk=legislator_id)
    if index == 'proposal':
        query_p = Q(date__gte=ly.term_start,legislator_proposal__priproposer=True)
        compare_obj = Proposal.objects.filter(query_p & Q(proposer__enable=True)).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Proposal.objects.filter(query_p & Q(proposer__id=legislator_id)).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Proposal.objects.filter(date__gte=ly.term_start).dates('date','month')
        obj = list_union(month_list,obj_q)
    elif index == 'vote':
        compare_obj = Vote.objects.filter(date__gte=ly.term_start).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Vote.objects.filter(date__gte=ly.term_start,voter__id=legislator_id,legislator_vote__decision__isnull=False).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Vote.objects.filter(date__gte=ly.term_start).dates('date','month')
        obj = list_union(month_list,obj_q)
    elif index == 'ly':
        compare_obj = Attendance.objects.filter(legislator_id=legislator_id,category=0).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Attendance.objects.filter(legislator_id=legislator_id,category=0,presentNum=1).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Attendance.objects.filter(date__gte=ly.term_start,category=0).dates('date','month')
        obj = list_union(month_list,obj_q)
    return render(request,'legislator/chart_personal_report.html', {'index':index,'ly':ly,'obj':obj,'compare_obj':compare_obj} )

def biller_detail(request,legislator_id,keyword_url):
    law,error,keyword,proposertype = None,False,None,False
    ly = get_object_or_404(Legislator, pk=legislator_id)
    if ly:
        if ly.hits:
            ly.hits = F('hits') + 1
        else:
            ly.hits = 1
        ly.save(update_fields=['hits'])
    query = Q(proposer__id=legislator_id,legislator_bill__priproposer=True)
    if 'proposertype' in request.GET:
        proposertype = request.GET['proposertype']
        if proposertype:
            query = Q(proposer__id=legislator_id)
    bills = Bill.objects.filter(query)
    laws = bills.values('law').distinct().order_by('law')
    if 'law' in request.GET:
        law = request.GET['law']
        if law:
            query = query & Q(law=law)
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        bills = bills.filter(query & reduce(operator.or_, (Q(motivation__icontains=x) for x in keyword.split()))).order_by('-proposalid')
        if bills:
            bills.update(hits=F('hits')+1)
    else:
        bills = bills.filter(query).order_by('-proposalid')
    return render(request,'legislator/biller_detail.html', {'laws':laws,'keyword_obj':keyword_list(3),'bills':bills,'ly':ly,'keyword':keyword,'error':error,'proposertype':proposertype})
