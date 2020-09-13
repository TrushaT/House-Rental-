from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Tenant,User,Owner


class OwnerSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','password1','password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_owner = True
        user.save()
        owner = Owner.objects.create(user=user)
        
        return user


class TenantSignUpForm(UserCreationForm):
    email = forms.EmailField()
    status_choices = Tenant.MARITIAL_STATUS_CHOICES
    maritial_status = forms.ChoiceField(choices = status_choices)
    Occupation = forms.CharField()


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','password1','password2','maritial_status','Occupation']
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tenant = True
        user.save()
        tenant = Tenant.objects.create(user=user)
        return user