from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *    
from .models import *
from django.contrib import messages
from django.http import HttpResponse
import urllib
import json
from .urls import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

KEY = '6Ldya-EUAAAAAE-BnwQPGjCjWQX5EFCqCKFkB1-K'

def home(request):
  
    if request.user.is_authenticated:

        if request.user.is_owner:
            return redirect('owner_home')
        else:
            return redirect('tenant_home')

    return render(request, 'users/home.html')

def tenant_home(request):

    tenant = User.objects.get(username = request.user.username)

    tenant = Tenant.objects.get(user=tenant)

    tenant_list = BookMarkPropertyList.objects.get(list_owner = tenant)

    form = None

    if request.method == 'GET': 

        all_properties = Property.objects.filter().order_by('-id')

        form = Searchproperty()

    elif request.method == 'POST':

        form = Searchproperty(request.POST)
        
        all_properties = Property.objects.all()

        if request.POST["location"]:
            all_properties = all_properties.filter(area = request.POST["location"])

        if request.POST["size"]:
            all_properties = all_properties.filter(property_size = request.POST["size"])

        if request.POST["Maxrent"]:
            all_properties = all_properties.filter(monthly_rent__lte = int(request.POST["Maxrent"]))

        if all_properties.count() == 0:
            all_properties = Property.objects.filter().order_by('-id')
            messages.error(request,"No Properties available for the given parameters")

    return render(request, 'users/tenant_home.html',{"all_properties" : all_properties, "tenant_list" : tenant_list, "form" : form })

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
               
                tenant = User.objects.get(username = form.cleaned_data.get("username"))

                tenant = Tenant.objects.get(user=tenant)

                tenant_list = BookMarkPropertyList.objects.create(list_owner = tenant)

                tenant_list.save()

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
        form = NewPropertyForm(request.POST, request.FILES)

        if form.is_valid():

            property_owner = Owner.objects.get(user=request.user)
            property_size = form.cleaned_data["property_size"]
            monthly_rent = form.cleaned_data["monthly_rent"]
            area = form.cleaned_data["area"]
            address_line_1 = form.cleaned_data["address_line_1"]
            address_line_2 = form.cleaned_data["address_line_2"]
            property_image = form.cleaned_data["property_image"]

            property = Property(property_owner=property_owner,
                property_size = property_size,
                monthly_rent = monthly_rent,
                area = area,
                address_line_1 = address_line_1,
                address_line_2 = address_line_2,
                property_image = property_image
            )

            property.save()

            messages.success(request,"Property Added Successfully !")

            return redirect("owner_home")


    else:
        form = NewPropertyForm()

    context = dict(form = form)

    return render(request,'users/new_property.html',context)

def delete_property(request, delete_id):

    property_to_delete = Property.objects.get(id=delete_id)

    property_to_delete.delete()

    owner = User.objects.get(username = request.user.username)

    owner = Owner.objects.get(user=owner)
    
    all_properties = Property.objects.filter(property_owner = owner).order_by('-id')

    messages.success(request,"Property Deleted Successfully !")

    return redirect('owner_home')

def update_property(request, update_id):
    
    property_to_update = Property.objects.get(id=update_id)

    if request.method == 'POST':
        form = UpdatePropertyForm(request.POST,request.FILES,instance=property_to_update)

        if form.is_valid():

            form.save()

            messages.success(request,"Details Updated Successfully !")

            return redirect('owner_home')

    elif request.method == 'GET':
        form = UpdatePropertyForm(instance=property_to_update)

    context = {
        "form" : form,
        "propertyid" : update_id,
    }

    return render(request,"users/update_property.html",context)

def bookmark(request, bookmark_id):

    tenant = User.objects.get(username = request.user.username)

    tenant = Tenant.objects.get(user=tenant)

    tenant_list = BookMarkPropertyList.objects.get(list_owner = tenant)

    bookmarked_property = Property.objects.get(id=bookmark_id)

    tenant_list.bookmarked_properties.add(bookmarked_property)
    tenant_list.save()

    messages.success(request,"Property Bookmarked Successfully !")

    return redirect('tenant_home')

def remove_bookmark(request, bookmark_id):

    tenant = User.objects.get(username = request.user.username)

    tenant = Tenant.objects.get(user=tenant)

    tenant_list = BookMarkPropertyList.objects.get(list_owner = tenant)

    bookmarked_property = Property.objects.get(id=bookmark_id)

    tenant_list.bookmarked_properties.remove(bookmarked_property)
    tenant_list.save()

    messages.success(request,"Property Bookmarked Removed Successfully !")

    return redirect('tenant_home')

def tenantupdate(request):

    tenant = User.objects.get(username = request.user.username)

    tenant = Tenant.objects.get(user=tenant)

    if request.method == 'POST':

        form = TenantUpdateForm(request.POST,instance=tenant)

        if form.is_valid():

            form.save()

            messages.success(request,"Details Updated Successfully !")

            return redirect('tenant_home')

    else:
       
        form = TenantUpdateForm(instance=tenant)

    return render(request, 'users/tenantupdate.html', {"form" : form})

def tenant_profile(request):

    tenant = User.objects.get(username = request.user.username)

    tenant = Tenant.objects.get(user=tenant)

    tenant_list = BookMarkPropertyList.objects.get(list_owner = tenant)

    all_properties = tenant_list.bookmarked_properties.all()

    context = {"all_properties" : all_properties, "tenant_list" : tenant_list, "tenant" : tenant}

    return render(request,"users/tenantprofile.html",context)

def notify_owner(request, notify_property_id):

    notify_property = Property.objects.get(id=notify_property_id)
    
    property_owner = notify_property.property_owner

    tenant = User.objects.get(username = request.user.username)

    tenant = Tenant.objects.get(user=tenant)

    subject = 'Someone has shown interest in your Property !'

    message = f"{tenant.user.username} is interested in your property.\n Occupation : {tenant.Occupation}.\n Marital Status : {tenant.maritial_status}.\n Phone Number : {tenant.phone_number}.\n"

    temp = "\n Details of the Property.\n"

    temp += f"Property Size : {notify_property.property_size}.\n Area : {notify_property.area}.\n Monthly Rent : {notify_property.monthly_rent}"

    temp += "\n Please contact as soon as possible\n"

    message +=  temp

    email_from = settings.EMAIL_HOST_USER

    recipient_list = [property_owner.user.email]

    send_mail(subject, message, email_from, recipient_list) 

    messages.success(request,"Your request is sent to the Owner")

    return redirect('tenant_home')