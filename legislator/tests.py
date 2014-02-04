# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse


class SimpleTest(TestCase):
    def test_index(self):
        for arg in ['biller', 'conscience_vote', 'committee', 'district', 'notvote']:
            response = self.client.get(reverse('legislator:index', args=(arg,)))
            self.assertEqual(response.status_code, 200)
            #self.assertContains(response, "No polls are available.")
            #self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_chart_report(self):
        for arg in ['biller', 'conscience_vote', 'vote', 'proposal', 'ly', 'committee', 'attend_committee']:
            response = self.client.get(reverse('legislator:chart_report', args=(arg,)))
            self.assertEqual(response.status_code, 200)
            #self.assertContains(response, "No polls are available.")
            #self.assertQuerysetEqual(response.context['latest_question_list'], [])
