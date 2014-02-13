# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Proposal, Legislator_Proposal
from legislator.models import Legislator, LegislatorDetail
from sittings.models import Sittings


class ProposalTest(TestCase):
    def setUp(self):
        Legislator.objects.create(uid=1, name=u"王金平")
        LegislatorDetail.objects.create(legislator_id=1, ad=8, name=u'王金平', party=u'中國國民黨', caucus=u'中國國民黨', constituency='全國不分區', county='全國不分區', in_office=True, hits=0)
        Sittings.objects.create(uid="08-01-YS-01", date="2012-02-01", ad=8, session=1)
        Proposal.objects.create(uid="08-01-YS-01-001", sitting_id="08-01-YS-01", proposal_seq="001", content="test content", hits=0, likes=0, dislikes=0)
        Legislator_Proposal.objects.create(legislator_id=1, proposal_id="08-01-YS-01-001", priproposer=True)

    def test_proposals(self):
        for keyword in [' ', u'test']:
            response = self.client.get(reverse('proposal:proposals', kwargs={"keyword_url": keyword}))
            self.assertEqual(response.status_code, 200)

    def test_proposal(self):
        response = self.client.get(reverse('proposal:proposal', kwargs={"proposal_id": "08-01-YS-01-001"}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('proposal:proposal', kwargs={"proposal_id": "not_exist_id"}))
        self.assertEqual(response.status_code, 302)
