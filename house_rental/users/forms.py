from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *
from crispy_forms.helper import FormHelper
from django.core.validators import MinValueValidator 

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

class NewPropertyForm(forms.Form):

    property_size = forms.ChoiceField(choices=Property.size_choices)
    monthly_rent = forms.IntegerField(validators=[MinValueValidator(1)])
    area = forms.ChoiceField(choices=Property.area_choices)
    address_line_1 = forms.CharField(max_length = 100)
    address_line_2 = forms.CharField(max_length = 100) 

    class Meta:
        model = Property
        fields = ['property_size', 'monthly_rent','area','address_line_1','address_line_2']

    def __init__(self, *args, **kwargs):
        super(NewPropertyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False