# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Bill, Legislator_Bill
from legislator.models import Legislator, LegislatorDetail


class BillTest(TestCase):
    def setUp(self):
        Bill.objects.create(uid="08-01-YS-01-001", api_bill_id="08-01-YS-01", abstract="test content")

    def test(self):
        for arg in ['normal', 'rejected']:
            for keyword in [' ', u'test']:
                response = self.client.get(reverse('bill:bills', kwargs={"index": arg, "keyword_url": keyword}))
                self.assertEqual(response.status_code, 200)
