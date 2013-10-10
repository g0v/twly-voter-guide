# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from legislator.models import Legislator,Proposal,Vote,Politics,Legislator_Vote,Keyword,Attendance,Issue,Bill
from django.db.models import Count,Sum,F,Q
import operator,re
from itertools import chain

def last_update_time():
    return '2013-10-04'
def district_list():
    return ["山地原住民","台中市","台北市","台東縣","台南市","平地原住民","全國不分區","宜蘭縣","花蓮縣","金門縣","南投縣","屏東縣","苗栗縣","桃園縣","高雄市","基隆市","連江縣","雲林縣","新北市","新竹市","新竹縣","僑居國外國民","嘉義市","嘉義縣","彰化縣","澎湖縣"]
def committee_list():
    return [u'\u5167\u653f', u'\u53f8\u6cd5\u53ca\u6cd5\u5236', u'\u5916\u4ea4\u53ca\u570b\u9632', u'\u4ea4\u901a', u'\u793e\u6703\u798f\u5229\u53ca\u885b\u751f\u74b0\u5883', u'\u8ca1\u653f', u'\u6559\u80b2\u53ca\u6587\u5316', u'\ufeff\u7d93\u6fdf']

def index(request,index):
    error, proposertype, query = None, False, Q(enable=True)
    outof_ly_list = Legislator.objects.filter(enable=False).order_by('disableReason')
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
                query = query & Q(legislator_bill__priproposer=True)
                no_count_list = Legislator.objects.filter(name_query).exclude(id__in=ly_list.values_list('id', flat=True))
        else:
            query = query & Q(legislator_bill__priproposer=True)
        ly_list = Legislator.objects.filter(query).annotate(totalNum=Count('legislator_bill__id')).exclude(totalNum=0).order_by('-totalNum')
        no_count_list = Legislator.objects.filter(name_query).exclude(id__in=ly_list.values_list('id', flat=True))
        #ly_list = list(chain(ly_list, no_count_list))
        return render(request,'legislator/index_ordered.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'no_count_list':no_count_list,'proposertype':proposertype,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})
    elif index == 'conscience_vote':
        ly_list = Legislator.objects.filter(query,legislator_vote__conflict=True).annotate(totalNum=Count('legislator_vote__id')).order_by('-totalNum','party')
        no_count_list = Legislator.objects.filter(name_query).exclude(id__in=ly_list.values_list('id', flat=True)).order_by('party')
        #ly_list = list(chain(ly_list, no_count_list))
        return render(request,'legislator/index_ordered.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'no_count_list':no_count_list,'proposertype':proposertype,'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})
    elif index == 'notvote':
        ly_obj = Legislator.objects.filter(query).defer('enableSession','disableReason')
        ly_list = sorted(ly_obj, key=lambda a: a.notvote)
        return render(request,'legislator/index_ordered.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})
    elif index == 'committee':
        ly_list = Legislator.objects.filter(query).order_by('committee').defer('enableSession','disableReason')
        return render(request,'legislator/index_committee.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})
    elif index == 'district':
        ly_list = Legislator.objects.filter(query).order_by('district').defer('enableSession','disableReason')
        return render(request,'legislator/index_district.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'ly_list': ly_list,'outof_ly_list': outof_ly_list,'index':index,'error':error,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})
    else:
        return HttpResponseRedirect('/legislator/biller/')

def index_district(request,index):
    ly_list = Legislator.objects.filter(enable=True,district=index).order_by('eleDistrict').defer('enableSession','disableReason')
    return render(request,'legislator/index_filter.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'ly_list': ly_list,'type':'district','index':index,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def index_committee(request,index):
    ly_list = Legislator.objects.filter(enable=True,committee=index).order_by('district').defer('enableSession','disableReason')
    return render(request,'legislator/index_filter.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'ly_list': ly_list,'type':'committee','index':index,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

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
    keyword_obj = Keyword.objects.filter(category=1,valid=True).order_by('-hits')[:5]
    return render(request,'legislator/proposer_detail.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'keyword_obj':keyword_obj,'proposal':proposal,'ly':ly,'keyword':keyword,'error':error,'proposertype':proposertype,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def proposal(request,proposal_id):
    proposal = Proposal.objects.select_related().get(pk=proposal_id)
    return render(request,'legislator/proposal.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'proposal': proposal,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def proposals(request,keyword_url):
    keyword,proposal,error = None,None,False
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        proposal = Proposal.objects.filter(reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-date','-pk').defer('sessionPrd','session')
        if proposal:
            proposal.filter(hits__isnull=False).update(hits=F('hits')+1)
            proposal.filter(hits__isnull=True).update(hits=1)
            keyword_obj = Keyword.objects.filter(category=1,content=keyword)
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            elif not keyword_url:
                k = Keyword(content=keyword,category=1,valid=True,hits=1)
                k.save()
    else:
        proposal = Proposal.objects.all().order_by('-date','-pk')[:10]
    keyword_obj = Keyword.objects.filter(category=1,valid=True).order_by('-hits')[:5]
    return render(request,'legislator/proposals.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'proposal':proposal,'keyword':keyword,'error':error,'keyword_obj':keyword_obj,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def proposals_related_to_issue(request,issue_id):
    keyword, proposal = None, None
    keyword = Issue.objects.values_list('title', flat=True).get(pk=issue_id)
    if issue_id:
        proposal = Proposal.objects.filter(issue_proposal__issue_id=issue_id).order_by('date','-pk')
    keyword_obj = Keyword.objects.filter(category=1,valid=True).order_by('-hits')[:5]
    return render(request,'legislator/proposals.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'keyword':keyword,'proposal':proposal,'keyword_obj':keyword_obj,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def votes(request,keyword_url,index='normal'):
    keyword,votes,error = None,None,False
    if index == 'conscience':
        query = Q(conflict=True)
    else:
        query = Q()
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        votes = Vote.objects.filter(query & reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-date','-pk')
        if votes:
            #votes.filter(hits__isnull=False).update(hits=F('hits')+1)
            #votes.filter(hits__isnull=True).update(hits=1)
            keyword_obj = Keyword.objects.filter(category=2,content=keyword)
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            elif not keyword_url:
                k = Keyword(content=keyword,category=2,valid=True,hits=1)
                k.save()
    else:
        votes = Vote.objects.filter(query).order_by('-date','-pk')
    keyword_obj = Keyword.objects.filter(category=2,valid=True).order_by('-hits')[:5]
    date_list = votes.values('date').distinct().order_by('-date')
    return render(request,'legislator/votes.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'votes': votes,'index':index,'keyword':keyword,'error':error,'keyword_obj':keyword_obj,'date_list':date_list,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def votes_related_to_issue(request,issue_id):
    keyword, votes, index = None, None, 'normal'
    keyword = Issue.objects.values_list('title', flat=True).get(pk=issue_id)
    if issue_id:
        votes = Vote.objects.filter(issue_vote__issue_id=issue_id).order_by('date','-pk')
    keyword_obj = Keyword.objects.filter(category=2,valid=True).order_by('-hits')[:5]
    date_list = votes.values('date').distinct().order_by('-date')
    return render(request,'legislator/votes.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'votes': votes,'index':index,'keyword':keyword,'keyword_obj':keyword_obj,'date_list':date_list,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def votes_date(request,date_url):
    keyword,votes,error = None,None,False
    if date_url:
        vote_date = date_url.strip()
    if vote_date:
        votes = Vote.objects.filter(date=vote_date).order_by('-pk')
    else:
        votes = Vote.objects.all().order_by('-date','-pk')
    keyword_obj = Keyword.objects.filter(category=2,valid=True).order_by('-hits')[:5]
    date_list = Vote.objects.values('date').distinct().order_by('-date')
    return render(request,'legislator/votes.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'votes': votes,'keyword':keyword,'error':error,'keyword_obj':keyword_obj,'date_list':date_list,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def vote_detail(request,vote_id):
    nvotes = Vote.objects.count()
    vote = Vote.objects.select_related().get(pk=vote_id)
    if vote:
        if vote.hits:
            vote.hits = F('hits') + 1
        else:
            vote.hits = 1
        vote.save(update_fields=['hits'])
        ly_notvote = Legislator.objects.exclude(id__in = vote.voter.values_list('id', flat=True)).filter(enable=True,enabledate__lt=vote.date).order_by('party')
        vote_addup = Legislator_Vote.objects.filter(vote_id=vote_id).values('decision').annotate(Count('legislator', distinct=True))
    return render(request,'legislator/vote_detail.html', {'current_url':'http://twly.herokuapp.com'+request.get_full_path(),'vote':vote,'nvotes':nvotes,'ly_notvote':ly_notvote,'vote_addup': vote_addup,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

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
    keyword_obj = Keyword.objects.filter(category=2,valid=True).order_by('-hits')[:5]
    return render(request,'legislator/voter_detail.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'keyword_obj':keyword_obj,'ly':ly,'index':index,'votes':votes,'keyword':keyword,'error':error,'vote_addup':vote_addup,'notvote':notvote,'notvote_votelist':notvote_votelist,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def ly_politics(request, legislator_id):
    ly = Legislator.objects.get(pk=legislator_id)
    if ly.eleDistrict == u'全國不分區':
        politics = Politics.objects.filter(party=ly.party).order_by('id')
        nodistrict = True
    else:
        politics = Politics.objects.filter(legislator_id=legislator_id).order_by('id')
        nodistrict = False
    return render(request,'legislator/ly_politics.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'ly':ly,'politics':politics,'nodistrict':nodistrict,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def chart_report(request,index='ly_hit'):
    ly_obj, ly_name, vote_obj,title,content,compare = [], [], [], None, None, None
    if index == 'vote':
        compare = Vote.objects.count()
        ly_obj = Legislator.objects.filter(enable=True)
        ly_obj = sorted(ly_obj, key=lambda a: a.notvote, reverse=True)[:10]
        ly_name = [ly.name for ly in ly_obj]
        title, content = u'立法院表決缺席前十名', u'每一次會議的最後會進行表決，可和立法院開會缺席交叉比較，為何開會有出席但沒有參加表決？(點選立委名字可看立委個人圖表)'
    elif index == 'conscience_vote':
        compare = Vote.objects.count()
        ly_obj = Legislator.objects.filter(enable=True,legislator_vote__conflict=True).annotate(totalNum=Count('legislator_vote__id')).order_by('-totalNum','party')[:10]
        ly_name = [ly.name for ly in ly_obj]
        title, content = u'脫黨投票次數前十名', u'點選立委名字可看立委脫黨投票的表決內容'
    elif index == 'biller':
        compare = "{0:.2f}".format(Bill.objects.count()/113.0)
        ly_obj = Legislator.objects.filter(enable=True,legislator_bill__priproposer=True).annotate(totalNum=Count('legislator_bill__id')).order_by('-totalNum','party')[:10]
        ly_name = [ly.name for ly in ly_obj]
        title, content = u'法條修正草案數前十名', u'立委在委員會中通過的法條修正草案數(點選立委名字可看立委個人提出的法案條修正草案)'
    elif index == 'proposal':
        compare = "{0:.2f}".format(Proposal.objects.count()/113.0)
        ly_obj = Legislator.objects.filter(enable=True,legislator_proposal__priproposer=True).annotate(totalNum=Count('legislator_proposal__id')).order_by('-totalNum','party')[:10]
        ly_name = [ly.name for ly in ly_obj]
        title, content = u'附帶決議、臨時提案數前十名', u'立委在委員會中提出的法案數，此處只有主提案人才會記數(點選立委名字可看立委個人圖表)'
    elif index == 'committee':
        ly_obj = Legislator.objects.filter(enable=True,attendance__category=1).annotate(totalNum=Sum('attendance__unpresentNum')).order_by('-totalNum','party')[:10]
        ly_name = [ly.name for ly in ly_obj]
        title, content = u'委員會開會缺席前十名', u'委員會是法案推行的第一關卡，立委需在委員會提出法案的增修(點選立委名字可看立委個人圖表)'
    elif index == 'ly':
        compare = Attendance.objects.values('session').filter(category=0).distinct().count()
        ly_obj = Legislator.objects.filter(enable=True,attendance__category=0).annotate(totalNum=Sum('attendance__unpresentNum')).order_by('-totalNum','party')[:10]
        ly_name = [ly.name for ly in ly_obj]
        title, content = u'立法院開會缺席前十名', u'立委須參加立法院例行會議，在會議中進行質詢、法案討論表決、人事表決等重要工作(點選立委名字可看立委個人圖表)'
    elif index == 'ly_hit':
        ly_obj = Legislator.objects.filter(enable=True,hits__isnull=False).order_by('-hits','party')[:10]
        ly_name = ly_obj.values_list('name', flat=True)
        title, content = u'點閱次數前十名', u'各立委在本站點閱次數排行'
    elif index == 'nvote_gbdate':
        vote_obj = Vote.objects.values('date','session').annotate(totalNum=Count('id', distinct=True)).order_by('date')
        title = u'立法院表決數依日期分組'
    elif index == 'nvote_gbmonth':
        vote_obj = Vote.objects.extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(totalNum=Count('id', distinct=True)).order_by('year','month')
        title = u'立法院表決數依月份分組'
    else:
        ly_obj = Legislator.objects.filter(enable=True,hits__isnull=False).order_by('-hits')[:10]
        ly_name = ly_obj.values_list('name', flat=True)
        title, content = u'立委點閱次數前十名', u'各立委在本站點閱次數排行'
    return render(request,'legislator/chart_report.html', {'current_url':'http://twly.herokuapp.com'+request.get_full_path(),'compare':compare,'title':title,'content':content,'index':index,'vote_obj':vote_obj,'ly_name': list(ly_name),'ly_obj':ly_obj,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()} )

def reference(request):
    return render(request,'legislator/reference.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})
def about(request):
    nvotes = Vote.objects.count()
    nproposals = Proposal.objects.count()
    nbills = Bill.objects.count()
    return render(request,'legislator/about.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'nvotes':nvotes,'nproposals':nproposals,'nbills':nbills,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

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
    query_c = Q(legislator_id=legislator_id,category=1,unpresentNum=1)
    if index == 'proposal':
        query_p = Q(legislator_proposal__legislator_id=legislator_id,legislator_proposal__priproposer=True)
        compare_obj = Proposal.objects.filter(legislator_proposal__priproposer=True,proposer__enable=True).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Proposal.objects.filter(query_p).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Proposal.objects.dates('date','month')
        obj = list_union(month_list,obj_q)
    elif index == 'vote':
        compare_obj = Vote.objects.extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Vote.objects.filter(voter__id=legislator_id).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Vote.objects.dates('date','month')
        obj = list_union(month_list,obj_q)
    elif index == 'ly':
        compare_obj = Attendance.objects.filter(legislator_id=legislator_id,category=0).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        obj_q = Attendance.objects.filter(legislator_id=legislator_id,category=0,presentNum=1).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        month_list = Attendance.objects.filter(category=0).dates('date','month')
        obj = list_union(month_list,obj_q)
    #elif index == 'committee':
        #query_c = Q(legislator_id=legislator_id,category=1,unpresentNum=1)
        #compare_obj = Attendance.objects.filter(legislator_id=legislator_id,category=1).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(Count('id', distinct=True)).order_by('year','month')
        #obj = Attendance.objects.filter(query_c).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"}).values('year','month').annotate(n=Count('id', distinct=True)).order_by('year','month')
    return render(request,'legislator/chart_personal_report.html', {'current_url':'http://twly.herokuapp.com'+request.get_full_path(),'index':index,'ly':ly,'obj':obj,'compare_obj':compare_obj,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()} )

def issues(request):
    issues = Issue.objects.select_related().order_by('-hits')
    issue = issues[0]
    return render(request,'legislator/issue.html', {'current_url':'http://twly.herokuapp.com'+request.get_full_path(),'issues':issues,'issue':issue,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def issue(request,issue_id):
    issues = Issue.objects.select_related().order_by('-hits')
    issue = issues.get(pk=issue_id)
    if issue:
        issue.hits = F('hits') + 1
        issue.save(update_fields=['hits'])
    return render(request,'legislator/issue.html', {'current_url':'http://twly.herokuapp.com'+request.get_full_path(),'issues':issues,'issue':issue,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def bills(request,keyword_url):
    law, keyword, query = None, None, Q()
    bills = Bill.objects.all()
    laws = bills.values('law').distinct().order_by('law')
    if 'law' in request.GET:
        law = request.GET['law']
        if law:
            query = Q(law=law)
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        bills = bills.filter(reduce(operator.or_, (Q(description__icontains=x) for x in keyword.split())) | reduce(operator.or_, (Q(motivation__icontains=x) for x in keyword.split()))).order_by('-proposalid')
        if bills:
            keyword_obj = Keyword.objects.filter(category=3,content=keyword.strip())
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            else:
                k = Keyword(content=keyword.strip(),category=3,valid=True,hits=1)
                k.save()
    else:
        bills = bills.filter(query).order_by('-proposalid')
    keyword_obj = Keyword.objects.filter(category=3,valid=True).order_by('-hits')[:5]
    return render(request,'legislator/bills.html', {'current_url':'http://twly.herokuapp.com'+request.get_full_path(),'keyword_obj':keyword_obj,'laws':laws,'law':law,'keyword':keyword,'bills':bills,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def bills_related_to_issue(request,issue_id):
    keyword, bills = None, None
    keyword = Issue.objects.values_list('title', flat=True).get(pk=issue_id)
    if issue_id:
        bills = Bill.objects.filter(issue_bill__issue_id=issue_id).order_by('date','-pk')
    keyword_obj = Keyword.objects.filter(category=3,valid=True).order_by('-hits')[:5]
    return render(request,'legislator/bills.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'keyword':keyword,'bills':bills,'keyword_obj':keyword_obj,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

def bill_detail(request,bill_id,proposal_id):
    bill = Bill.objects.filter(billid=bill_id,proposalid=proposal_id)[0]
    if bill:
        bill.hits = F('hits') + 1
    return render(request,'legislator/bill_detail.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'bill': bill,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})

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
    keyword_obj = Keyword.objects.filter(category=3,valid=True).order_by('-hits')[:5]
    return render(request,'legislator/biller_detail.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'laws':laws,'keyword_obj':keyword_obj,'bills':bills,'ly':ly,'keyword':keyword,'error':error,'proposertype':proposertype,'district':district_list(),'committee':committee_list(),'last_update':last_update_time()})
