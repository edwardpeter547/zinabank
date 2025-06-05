from django.test import TestCase
from core_apps.user_auth.models import User as CoreUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.conf import settings
from unittest.mock import patch
from core_apps.user_auth.emails import send_account_locked_email
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user: CoreUser = User.objects.create_user(
            id_no="123456789",
            email="testuser@gmail.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            role="user",
            otp="123456",
            otp_expiry_time=timezone.now() + timezone.timedelta(minutes=5)
        )
    
    def test_verify_otp_success(self):
        """
        Test that the OTP verification process succeeds when provided with valid input.
        """
        self.assertTrue(self.user.verify_otp(otp="123456"))

    def test_verify_otp_failure(self):
        """
        Test that the OTP verification process fails when provided with invalid input.
        """
        self.assertFalse(self.user.verify_otp(otp="wrongotp"))

    def test_verify_otp_expired(self):
        """
        Test that the OTP verification fails when the OTP has expired.
        """
        self.user.otp_expiry_time = timezone.now() - timezone.timedelta(minutes=1)
        self.user.save()
        self.assertFalse(self.user.verify_otp(otp="123456"))

    