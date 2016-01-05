# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Bill, Legislator_Bill
from legislator.models import Legislator, LegislatorDetail


class BillTest(TestCase):
    def setUp(self):
        Bill.objects.create(uid="08-01-YS-01-001", ad=8, data={'test': 'test'})

    def test(self):
        response = self.client.get(reverse('bill:bills'))
        self.assertEqual(response.status_code, 200)
