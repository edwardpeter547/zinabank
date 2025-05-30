import random
import string
from django.conf import settings
from typing import Any, Optional
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def generate_username() -> str:
    bank_name: str = settings.BANK_NAME
    prefix: str = "".join([word[0] for word in bank_name.split()]).upper()
    remaining_length: int = 12 - len(prefix) - 1
    random_chars: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=remaining_length))
    return f"{prefix}-{random_chars}"


def validate_email_address(email: str) -> None:
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_("Enter a valid email address."))
    


class UserManager(DjangoUserManager):
    def _create_user(self, email: str, password: str, **extra_fields: Any):
        if not email:
            raise ValueError(_("An email address must be provided"))
        
        if not password:
            raise ValueError(_("A password must be provided."))
        
        username = generate_username()
        email = self.normalize_email(email)
        validate_email_address(email)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: Optional[str]=None, **extra_fields: Any):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email: str, password: Optional[str]=None, **extra_fields: Any):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser must have is_staff=True"))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must have is_superuser=True"))
        
        return self._create_user(email, password, **extra_fields)