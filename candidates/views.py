# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.db import connections

from .models import Candidates, Terms
from legislator.models import LegislatorDetail


def counties(request, ad):
    regions = [
        {"region": "北部", "counties": ["臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹縣", "新竹市"]},
        {"region": "中部", "counties": ["苗栗縣", "臺中市", "彰化縣", "雲林縣", "南投縣"]},
        {"region": "南部", "counties": ["嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣"]},
        {"region": "東部", "counties": ["花蓮縣", "臺東縣"]},
        {"region": "離島", "counties": ["澎湖縣", "金門縣", "連江縣"]},
        {"region": "全島", "counties": ["山地原住民", "平地原住民", "全國不分區", "僑居國外國民"]}
    ]
    return render(request, 'candidates/counties.html', {'ad': ad, 'regions': regions})

def districts(request, ad, county):
    districts = Terms.objects.filter(ad=ad, county=county)\
                                  .values('constituency', 'district')\
                                  .annotate(candidates=Count('id'))\
                                  .order_by('constituency')
    if len(districts) == 1:
        return HttpResponseRedirect(reverse('candidates:district', kwargs={'ad': ad, 'county': county, 'constituency': 1}))
    return render(request, 'candidates/districts.html', {'ad': ad, 'county': county, 'districts': districts})

def district(request, ad, county, constituency):
    if county == u'全國不分區' or county == u'僑居國外國民':
        parties = Terms.objects.filter(ad=ad, county=county, constituency=constituency).distinct('party').values_list('party', flat=True)
        party = request.GET.get('party', '')
        qs = Q(party=party) if party else Q()
        candidates = Terms.objects.select_related('latest_term', 'legislator')\
                                  .filter(Q(ad=ad, county=county, constituency=constituency) & qs)\
                                  .extra(select={
                                      'latest_ad': "select max(ld.ad) from legislator_legislatordetail ld where id = candidates_terms.legislator_id or id = candidates_terms.latest_term_id",
                                      'legislator_uid': "select ld.legislator_id from legislator_legislatordetail ld where id = candidates_terms.legislator_id or id = candidates_terms.latest_term_id limit 1",
                                  },)\
                                  .order_by('party', 'priority')
        return render(request, 'candidates/district_nonregional.html', {'ad': ad, 'county': county, 'candidates': candidates, 'parties': parties, 'party': party})
    else:
        county_changes = {"9": {u"桃園市": u"桃園縣"}}
        candidates_previous = Terms.objects.select_related('candidate', 'latest_term', 'legislator')\
                                           .filter(ad=int(ad)-1, county=county_changes.get(ad, {}).get(county, county), constituency=constituency)\
                                           .extra(select={
                                               'latest_ad': "select max(ld.ad) from legislator_legislatordetail ld where id = candidates_terms.legislator_id or id = candidates_terms.latest_term_id",
                                               'legislator_uid': "select ld.legislator_id from legislator_legislatordetail ld where id = candidates_terms.legislator_id or id = candidates_terms.latest_term_id limit 1",
                                           },)\
                                           .order_by('-votes')
        candidates = Terms.objects.select_related('latest_term', 'legislator')\
                                  .filter(ad=ad, county=county, constituency=constituency)\
                                  .extra(select={
                                      'latest_ad': "select max(ld.ad) from legislator_legislatordetail ld where id = candidates_terms.legislator_id or id = candidates_terms.latest_term_id",
                                      'legislator_uid': "select ld.legislator_id from legislator_legislatordetail ld where id = candidates_terms.legislator_id or id = candidates_terms.latest_term_id limit 1",
                                  },)\
                                  .order_by('legislator_uid')
        standpoints = {}
        for term in [candidates_previous, candidates]:
            for candidate in term:
                if candidate.latest_ad > 5 and candidate.legislator_uid:
                    terms_id = tuple(LegislatorDetail.objects.filter(legislator_id=candidate.legislator_uid).values_list('id', flat=True))
                    c = connections['default'].cursor()
                    qs = u'''
                        SELECT json_agg(row)
                        FROM (
                            SELECT
                                CASE
                                    WHEN lv.decision = 1 THEN '贊成'
                                    WHEN lv.decision = -1 THEN '反對'
                                    WHEN lv.decision = 0 THEN '棄權'
                                    WHEN lv.decision isnull THEN '沒投票'
                                END as decision,
                                s.title,
                                count(*) as times
                            FROM vote_legislator_vote lv
                            JOIN standpoint_standpoint s on s.vote_id = lv.vote_id
                            WHERE lv.legislator_id in %s AND s.pro = (
                                SELECT max(pro)
                                FROM standpoint_standpoint ss
                                WHERE ss.pro > 0 AND s.vote_id = ss.vote_id
                                GROUP BY ss.vote_id
                            )
                            GROUP BY s.title, lv.decision
                            ORDER BY times DESC
                            LIMIT 3
                        ) row
                    '''
                    c.execute(qs, [terms_id])
                    r = c.fetchone()
                    standpoints.update({candidate.id: r[0] if r else []})
        return render(request, 'candidates/district.html', {'ad': ad, 'county': county, 'candidates': candidates, 'candidates_previous': candidates_previous, 'standpoints': standpoints})

def political_contributions(request, id):
    candidate = get_object_or_404(Terms, id=id)
    return render(request, 'candidates/politicalcontributions.html', {'candidate': candidate})
