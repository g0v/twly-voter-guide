# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, Q

from .models import Candidates


def counties(request, ad):
    counties = Candidates.objects.filter(ad=ad)\
                                 .values('county')\
                                 .annotate(candidates=Count('id'))\
                                 .order_by('-candidates')
    return render(request, 'candidates/counties.html', {'ad': ad, 'counties': counties})

def districts(request, ad, county):
    districts = Candidates.objects.filter(ad=ad, county=county)\
                                  .values('constituency', 'district')\
                                  .annotate(candidates=Count('id'))\
                                  .order_by('constituency')
    if len(districts) == 1:
        return HttpResponseRedirect(reverse('candidates:district', kwargs={'ad': ad, 'county': county, 'constituency': 1}))
    return render(request, 'candidates/districts.html', {'ad': ad, 'county': county, 'districts': districts})

def district(request, ad, county, constituency):
    candidates = Candidates.objects.select_related('latest_term', 'legislator')\
                                   .filter(ad=ad, county=county, constituency=constituency)\
                                   .order_by('legislator_id', 'party')
    for candidate in candidates:
        if candidate.legislator_id:
            return render(request, 'candidates/district_result.html', {'ad': ad, 'county': county, 'candidates': candidates})
    return render(request, 'candidates/district.html', {'ad': ad, 'county': county, 'candidates': candidates})

def political_contributions(request, uid, ad):
    candidate = get_object_or_404(Candidates.objects.select_related('politicalcontributions'), ad=ad, uid=uid)
    return render(request, 'candidates/politicalcontributions.html', {'candidate': candidate})
