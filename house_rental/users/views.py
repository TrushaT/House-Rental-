from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import TenantSignUpForm, OwnerSignUpForm
from .models import User, Tenant
from django.contrib import messages


def home(request):
    if request.user.is_authenticated:
        if request.user.is_owner:
            return redirect('owner_home')
        else:
            return redirect('tenant_home')
    return render(request, 'users/home.html')

def tenant_home(request):
    return render(request, 'users/tenant_home.html')

def owner_home(request):
    return render(request, 'users/owner_home.html')




def tenant_register(request):
    if request.method == "POST":
        form = TenantSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"{username}, your account has been created! You can now login with your credentials!")
            return redirect('login')
    else:
        form = TenantSignUpForm()

    context = dict(form=form,user_type='Tenant')
    return render(request,'users/signup_form.html',context)

def owner_register(request):
    if request.method == "POST":
        form = OwnerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"{username}, your account has been created! You can now login with your credentials!")
            return redirect('login')
    else:
        form = OwnerSignUpForm()

    context = dict(form=form,user_type='Owner')
    return render(request,'users/signup_form.html',context)


        