# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db import connections

from .models import Candidates
from legislator.models import LegislatorDetail


def counties(request, ad):
    counties = Candidates.objects.filter(ad=ad)\
                                 .values('county')\
                                 .annotate(candidates=Count('uid'))\
                                 .order_by('-candidates')
    return render(request, 'candidates/counties.html', {'ad': ad, 'counties': counties})

def districts(request, ad, county):
    districts = Candidates.objects.filter(ad=ad, county=county)\
                                  .values('constituency', 'district')\
                                  .annotate(candidates=Count('uid'))\
                                  .order_by('constituency')
    if len(districts) == 1:
        return HttpResponseRedirect(reverse('candidates:district', kwargs={'ad': ad, 'county': county, 'constituency': 1}))
    return render(request, 'candidates/districts.html', {'ad': ad, 'county': county, 'districts': districts})

def district(request, ad, county, constituency):
    candidates = Candidates.objects.select_related('latest_term', 'legislator')\
                                   .filter(ad=ad, county=county, constituency=constituency)\
                                   .extra(select={
                                       'latest_ad': "select max(ld.ad) from legislator_legislatordetail ld where id = candidates_candidates.legislator_id or id = candidates_candidates.latest_term_id",
                                       'legislator_uid': "select ld.legislator_id from legislator_legislatordetail ld where id = candidates_candidates.legislator_id or id = candidates_candidates.latest_term_id limit 1",
                                   },)\
                                   .order_by('number')
    standpoints = {}
    for candidate in candidates:
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
            standpoints.update({candidate.uid: r[0] if r else []})
    return render(request, 'candidates/district_result.html', {'ad': ad, 'county': county, 'candidates': candidates, 'standpoints': standpoints})
    return render(request, 'candidates/district.html', {'ad': ad, 'county': county, 'candidates': candidates})

def political_contributions(request, uid, ad):
    candidate = get_object_or_404(Candidates, ad=ad, uid=uid)
    return render(request, 'candidates/politicalcontributions.html', {'candidate': candidate})
