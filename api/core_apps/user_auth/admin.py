from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from core_apps.user_auth.models import User
from core_apps.user_auth.forms import UserChangeForm, UserCreationForm

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "role",
    ]

    list_filter = ["email", "is_staff", "is_active", "role"]

    search_fields = ["email", "username", "first_name", "last_name"]

    ordering = ["email"]

    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields":(
                    "username",
                    "email",
                    "password",
                )
            }
        ),
        (
            _("Personal Information"),
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "id_no", 
                    "role",
                )
            },
        ),
        (
            _("Account Status"),
            {
                "fields": (
                    "account_status",
                    "failed_login_attempts",
                    "last_failed_login",
                )
            },
        ),
        (
            _("Security"),
            {
                "fields": ("security_question", "security_answer")
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )


