from django.contrib.auth.forms import UserChangeForm as ZBankUserChangeForm
from django.contrib.auth.forms import UserCreationForm as ZBankUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core_apps.user_auth.models import User

def perform_clean(form, data):
    is_superuser = data.get("is_superuser")
    security_question = data.get("security_question")
    security_answer = data.get("security_answer")

    if not is_superuser:
        if not security_question:
            form.add_error("security_question", _("A security question is required this user"))
        if not security_answer:
            form.add_error("security_answer", _("Please provide answer to security question"))
    
    return data

class UserCreationForm(ZBankUserCreationForm):
    class Meta:
        model = User
        fields = [
            "email", 
            "id_no", 
            "first_name", 
            "middle_name", 
            "last_name", 
            "security_question",
            "security_answer",
            "is_staff",
            "is_superuser",
        ]
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self._meta.model.objects.filter(email=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email
    
    def clean_id_no(self):
        id_no = self.cleaned_data.get("email")
        if self._meta.model.objects.filter(id_no=id_no).exists():
            raise ValidationError(_("A user with that ID number already exists."))
        return id_no
    
    def clean(self):
        data = super().clean()
        return perform_clean(form=self, data=data)
        
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    

class UserChangeForm(ZBankUserChangeForm):
    class Meta:
        model = User
        fields = [
            "email", 
            "id_no", 
            "first_name", 
            "middle_name", 
            "last_name", 
            "security_question",
            "security_answer",
            "is_staff",
            "is_superuser",
            "is_active",
        ]
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        users = self._meta.model.objects
        if users.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email

    def clean_id_no(self):
        id_no = self.cleaned_data.get("id_no")
        users = self._meta.model.objects
        if users.exclude(pk=self.instance.pk).filter(id_no=id_no).exists():
            raise ValidationError(_("A user with that ID number already exists."))
        return id_no
    
    def clean(self):
        data = super().clean()
        return perform_clean(form=self, data=data)
        