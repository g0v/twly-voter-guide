# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Legislator, LegislatorDetail


class StaticViewTest(TestCase):
    def test(self):
        for arg in ['about', 'reference']:
            response = self.client.get(reverse(arg))
            self.assertEqual(response.status_code, 200)

class LegislatorTest(TestCase):
    def setUp(self):
        Legislator.objects.create(uid=1, name=u"王金平")
        LegislatorDetail.objects.create(legislator_id=1, ad=8, name=u'王金平', party=u'中國國民黨', caucus=u'中國國民黨', constituency=0, county='全國不分區', in_office=True, vote_param={"abstain": 1, "disagree": 242, "not_voting": 62, "total": 400, "agree": 95, "conflict": 12}, bill_param={"chief": 58, "total": 469, "proposal": 138, "petition": 273}, attendance_param={"absent": 1, "total": 102})

    def test_index(self):
        for arg in ['conflict', 'not_voting']:
            response = self.client.get(reverse('legislator:index', kwargs={"index": arg}))
            self.assertEqual(response.status_code, 200)
        # homepage
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_counties(self):
        response = self.client.get(reverse('legislator:counties'))
        self.assertEqual(response.status_code, 200)

    def test_county(self):
        response = self.client.get(reverse('legislator:county', kwargs={"county": '全國不分區'}))
        self.assertEqual(response.status_code, 200)

    def test_legislator_personal_page(self):
        for arg in ['biller_detail', 'voter_detail', 'platformer_detail']:
            response = self.client.get(reverse('legislator:%s' % arg, kwargs={"legislator_id": 1, "ad": 8}))
            self.assertEqual(response.status_code, 200)
            # legislator_id not exist case
            response = self.client.get(reverse('legislator:%s' % arg, kwargs={"legislator_id": 0, "ad": 8}))
            self.assertEqual(response.status_code, 404)

    def test_chart_report(self):
        for arg in ['biller', 'conscience_vote', 'vote', 'ly']:
            response = self.client.get(reverse('legislator:chart_report', kwargs={"index": arg}))
            self.assertEqual(response.status_code, 200)
