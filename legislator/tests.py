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
        LegislatorDetail.objects.create(legislator_id=1, ad=8, name=u'王金平', party=u'中國國民黨', caucus=u'中國國民黨', constituency='全國不分區', county='全國不分區', in_office=True, hits=0)

    def test_index(self):
        for arg in ['biller', 'conscience_vote', 'committee', 'district', 'notvote']:
            #response = self.client.get(reverse('legislator:index', args=(arg,)))
            response = self.client.get(reverse('legislator:index', kwargs={"index": arg}))
            self.assertEqual(response.status_code, 200)
        # homepage
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # search legislator name
        for arg in [u'王', ' ']:
            response = self.client.get("%s?lyname=%s" % (reverse('legislator:index', kwargs={"index": "biller"}), arg))
            self.assertEqual(response.status_code, 200)
            response = self.client.get("%s?proposertype=" % reverse('legislator:index', kwargs={"index": "biller"}))
            self.assertEqual(response.status_code, 200)

    def test_district(self):
        response = self.client.get(reverse('legislator:index_district', kwargs={"index": '全國不分區'}))
        self.assertEqual(response.status_code, 200)

    def test_committee(self):
        response = self.client.get(reverse('legislator:index_committee', kwargs={"index": '經濟委員會'}))
        self.assertEqual(response.status_code, 200)

    def test_legislator_personal_page(self):
        for arg in ['biller_detail', 'proposer_detail', 'voter_detail', 'platformer_detail']:
            response = self.client.get(reverse('legislator:%s' % arg, kwargs={"legislator_id": 1}))
            self.assertEqual(response.status_code, 200)
            # legislator_id not exist case
            response = self.client.get(reverse('legislator:%s' % arg, kwargs={"legislator_id": 0}))
            self.assertEqual(response.status_code, 302)
        for arg in ['biller_detail', 'proposer_detail']:
            response = self.client.get("%s?proposertype=on" % reverse('legislator:%s' % arg, kwargs={"legislator_id": 1, "keyword_url": "test"}))
            self.assertEqual(response.status_code, 200)
        for arg in ['', 'conscience']:
            response = self.client.get("%s?notvote=on" % reverse('legislator:voter_detail', kwargs={"index": arg, "legislator_id": 1, "keyword_url": "test"}))
            self.assertEqual(response.status_code, 200)

    def test_chart_report(self):
        for arg in ['biller', 'conscience_vote', 'vote', 'proposal', 'ly', 'committee', 'attend_committee']:
            response = self.client.get(reverse('legislator:chart_report', kwargs={"index": arg}))
            self.assertEqual(response.status_code, 200)
