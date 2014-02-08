# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Bill


class BillTest(TestCase):
    def test(self):
        for arg in ['normal', 'rejected']:
            for keyword in [' ', u'test spilt']:
                response = self.client.get(reverse('bill:bills', kwargs={"index": arg, "keyword_url": keyword}))
                self.assertEqual(response.status_code, 200)
