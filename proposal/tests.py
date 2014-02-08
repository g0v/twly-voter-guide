# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Proposal


class ProposalTest(TestCase):
    def test(self):
        for keyword in [' ', u'test spilt']:
            response = self.client.get(reverse('proposal:proposals', kwargs={"keyword_url": keyword}))
            self.assertEqual(response.status_code, 200)
