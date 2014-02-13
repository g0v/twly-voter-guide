# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Vote, Legislator_Vote
from legislator.models import Legislator, LegislatorDetail
from sittings.models import Sittings


class VoteTest(TestCase):
    def setUp(self):
        Legislator.objects.create(uid=1, name=u"王金平")
        LegislatorDetail.objects.create(legislator_id=1, ad=8, name=u'王金平', party=u'中國國民黨', caucus=u'中國國民黨', constituency='全國不分區', county='全國不分區', in_office=True, hits=0)
        Sittings.objects.create(uid="08-01-YS-01", date="2012-02-01", ad=8, session=1)
        Vote.objects.create(uid="08-01-YS-01-001", sitting_id="08-01-YS-01", vote_seq="001", content="test content", hits=0, likes=0, dislikes=0, results={"abstain": 0, "not_voting": 4, "total": 113, "disagree": 46, "agree": 63})
        Legislator_Vote.objects.create(legislator_id=1, vote_id="08-01-YS-01-001", decision=1)

    def test_votes(self):
        for arg in ['normal', 'conscience']:
            for keyword in [' ', u'test']:
                response = self.client.get(reverse('vote:votes', kwargs={"index": arg, "keyword_url": keyword}))
                self.assertEqual(response.status_code, 200)

    def test_vote(self):
        response = self.client.get(reverse('vote:vote_detail', kwargs={"vote_id": "08-01-YS-01-001"}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('vote:vote_detail', kwargs={"vote_id": "not_exist_id"}))
        self.assertEqual(response.status_code, 302)
