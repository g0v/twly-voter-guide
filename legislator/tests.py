# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Legislator
from .models import LegislatorDetail
from committees.models import Legislator_Committees


class SimpleTest(TestCase):
    #fixtures = ['fixture.json']
    def test_index(self):
        for arg in ['biller', 'conscience_vote', 'committee', 'district', 'notvote']:
            print arg
            response = self.client.get(reverse('legislator:index', args=(arg,)))
            self.assertEqual(response.status_code, 200)
            #self.assertContains(response, "No polls are available.")
            #self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_each_district(self):
        for arg in LegislatorDetail.objects.filter(ad=8).values_list('county', flat=True):
            print arg
            response = self.client.get(reverse('legislator:index_district', args=(arg,)))
            self.assertEqual(response.status_code, 200)

    def test_chart_report(self):
        for arg in ['biller', 'conscience_vote', 'vote', 'proposal', 'ly', 'committee', 'attend_committee']:
            response = self.client.get(reverse('legislator:chart_report', args=(arg,)))
            self.assertEqual(response.status_code, 200)
