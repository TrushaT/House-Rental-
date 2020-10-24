from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *
from crispy_forms.helper import FormHelper
from django.core.validators import MinValueValidator 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder,HTML, Submit, Row, Column, Div, Reset, Field
from phonenumber_field.formfields import PhoneNumberField

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
    Occupation = forms.ChoiceField(choices = Tenant.OCCUPATION_CHOICES)
    phone_number = PhoneNumberField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','password1','password2','maritial_status','Occupation','phone_number']
   
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tenant = True
        user.save()
        maritial_status_data = self.cleaned_data["maritial_status"]
        occupaton_choice = self.cleaned_data["Occupation"]
        contact_number = self.cleaned_data["phone_number"]
        tenant = Tenant.objects.create(user=user,maritial_status = maritial_status_data, Occupation=occupaton_choice,phone_number=contact_number)
        return user

class TenantUpdateForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = ['maritial_status','Occupation','phone_number']

    def __init__(self, *args, **kwargs):
        super(TenantUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(

            Row(Column('maritial_status', css_class = "form-group col-md-6 mb-0 col-lg-2"),
                css_class='form-row'
            ),

            Row(Column('Occupation', css_class = "form-group col-md-6 mb-6 col-lg-3"),
                css_class='form-row'
            ),

            Row(Column('phone_number', css_class = "form-group col-md-6 mb-0 col-lg-2"),
                css_class='form-row'
            ),

            Row(Column(Submit('submit', 'Submit', css_class = 'col-lg-2 btn-success btn-border'),
                Reset('reset', 'Reset', css_class = 'col-lg-2 btn-primary btn-border')),
                css_class='form-row'
                )
        )

class NewPropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ['property_size','property_image','monthly_rent','area','address_line_1','address_line_2']

    def __init__(self, *args, **kwargs):
        super(NewPropertyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class UpdatePropertyForm(forms.ModelForm):

    class Meta:
        fields = ['monthly_rent','property_image','area','address_line_1','address_line_2']

        model = Property

    def __init__(self, *args, **kwargs):

        super(UpdatePropertyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(

            Row(Column('monthly_rent', css_class = "form-group col-md-6 mb-0 col-lg-2"),
                Column('area', css_class = "form-group col-md-6 mb-0 col-lg-2"),
                css_class='form-row'
            ),

            Row(Column('property_image', css_class = "form-group col-md-6 mb-6 col-lg-5"),
                css_class='form-row'
            ),

            Row(Column('address_line_1', css_class = "form-group  col-md-9 mb-6 col-lg-5"),
                css_class='form-row'
            ),

            Row(Column('address_line_2', css_class = "form-group  col-md-9 mb-6 col-lg-5"),
                css_class='form-row'
            ),

            Row(Column(Submit('submit', 'Submit', css_class = 'col-lg-2 btn-success btn-border'),
                Reset('reset', 'Reset', css_class = 'col-lg-2 btn-primary btn-border')),
                css_class='form-row'
                )
        )

class Searchproperty(forms.Form):    

    size_choices = Property.size_choices
    size_choices.insert(0, ('',''))

    area_choices = Property.area_choices
    area_choices.insert(0, ('',''))

    location = forms.ChoiceField(choices=area_choices, required = False, help_text = 'Location')
    size = forms.ChoiceField(choices=size_choices, required = False, help_text = 'House Size')
    Maxrent = forms.IntegerField(required = False, validators = [MinValueValidator(1)], help_text = 'Max Rent')

    def __init__(self, *args, **kwargs):
        super(Searchproperty, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        self.helper.layout = Layout(

            Row(Column('location', css_class = "form-group col-md-6 mb-0 col-lg-2"),
                Column('size', css_class = "form-group col-md-6 mb-0 col-lg-2"),
                Column('Maxrent', css_class = "form-group col-md-6 mb-0 col-lg-2"),
                Column(
                    HTML('<button type="submit" class="btn btn-primary btn-border">'
                    '<span class="fa fa-search"></span>Search ''</button>')
                    ),
                css_class='form-row '
                )
            )