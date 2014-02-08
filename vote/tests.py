# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Vote


class VoteTest(TestCase):
    def test(self):
        for arg in ['normal', 'conscience']:
            for keyword in [' ', u'test spilt']:
                response = self.client.get(reverse('vote:votes', kwargs={"index": arg, "keyword_url": keyword}))
                self.assertEqual(response.status_code, 200)
