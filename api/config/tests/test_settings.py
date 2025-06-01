from django.test import TestCase
from django.conf import settings
import datetime


class TestSettings(TestCase):
    def test_default_dates_are_valid(self):
        self.assertIsInstance(settings.DEFAULT_BIRTH_DATE, datetime.date)
        self.assertIsInstance(settings.DEFAULT_DATE, datetime.date)
        self.assertIsInstance(settings.DEFAULT_EXPIRY_DATE, datetime.date)