from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *
from .models import *
from django.contrib import messages
from django.http import HttpResponse
import urllib
import json
from django.contrib.auth.decorators import login_required

KEY = '6Ldya-EUAAAAAE-BnwQPGjCjWQX5EFCqCKFkB1-K'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_owner:
            return redirect('owner_home')
        else:
            return redirect('tenant_home')

    return render(request, 'users/home.html')

def tenant_home(request):

    all_properties = Property.objects.filter().order_by('-id')

    return render(request, 'users/tenant_home.html',{"all_properties" : all_properties})

def owner_home(request):
    
    owner = User.objects.get(username = request.user.username)

    owner = Owner.objects.get(user=owner)

    all_properties = Property.objects.filter(property_owner = owner).order_by('-id')

    return render(request, 'users/owner_home.html',{"all_properties" : all_properties})

def tenant_register(request):
    
    if request.method == "POST":

        form = TenantSignUpForm(request.POST)
        if form.is_valid():

            url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_response = request.POST.get("g-recaptcha-response")

            values = {
                'secret' : KEY,
                'response' : recaptcha_response
            }

            data = urllib.parse.urlencode(values).encode()

            req = urllib.request.Request(url, data=data)

            response = urllib.request.urlopen(req)

            result = json.loads(response.read().decode())

            if result["success"]:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request,f"{username}, your account has been created! You can now login with your credentials!")
                return redirect('login')

            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    else:
        form = TenantSignUpForm()

    context = dict(form=form,user_type='Tenant')
    return render(request,'users/signup_form.html',context)


def owner_register(request):

    if request.method == "POST":
        form = OwnerSignUpForm(request.POST)
        if form.is_valid():

            url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_response = request.POST.get("g-recaptcha-response")

            values = {
                'secret' : KEY,
                'response' : recaptcha_response
            }

            data = urllib.parse.urlencode(values).encode()

            req =  urllib.request.Request(url, data=data)

            response = urllib.request.urlopen(req)

            result = json.loads(response.read().decode())

            if result["success"]:

                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request,f"{username}, your account has been created! You can now login with your credentials!")
                return redirect('login')

            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    else:
        form = OwnerSignUpForm()

    context = dict(form=form,user_type='Owner')
    return render(request,'users/signup_form.html',context)

def new_property(request):

    if request.method == 'POST':
        form = NewPropertyForm(request.POST)

        if form.is_valid():

            property_owner = Owner.objects.get(user=request.user)
            property_size = form.cleaned_data["property_size"]
            monthly_rent = form.cleaned_data["monthly_rent"]
            area = form.cleaned_data["area"]
            address_line_1 = form.cleaned_data["address_line_1"]
            address_line_2 = form.cleaned_data["address_line_2"]

            property = Property(property_owner=property_owner,
                property_size = property_size,
                monthly_rent = monthly_rent,
                area = area,
                address_line_1 = address_line_1,
                address_line_2 = address_line_2
            )

            property.save()

            return redirect("owner_home")


    else:
        form = NewPropertyForm()

    context = dict(form = form)

    return render(request,'users/new_property.html',context)