from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.db import connection, IntegrityError, transaction

from .forms import LoginForm, RegisterForm, CreateFolderForm, CreateTableForm

# Create your views here.
from .models import CustomUser, FolFolRel, FolTabRel
from DataSet.views import home_view


def landing_view(request):
    return render(request, 'Users/landing.html')


def login_view(request):
    if request.method == "GET":
        return render(request, 'Users/login.html')
    else:
        loginForm = LoginForm(request.POST, request.FILES)
        if loginForm.is_valid():
            email = loginForm.cleaned_data['email']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                # Valid User
                username = user.username
                login(request, user)
                return redirect(home_view)
            else:
                return HttpResponse("Not a Valid User")

        return HttpResponse("Invalid Values")


def register_view(request):
    if request.method == 'GET':
        return render(request, 'Users/register.html', {
            'message': "",
            "Present": False
        })
    else:
        registerForm = RegisterForm(request.POST, request.FILES)
        if registerForm.is_valid():
            email = registerForm.cleaned_data['email']
            pass1 = registerForm.cleaned_data['password1']
            pass2 = registerForm.cleaned_data['password2']
            username = registerForm.cleaned_data['username']

            if pass1 == pass2:
                #  user valid
                try:
                    user = CustomUser.objects.create_user(email=email, password=pass1, username=username)
                    login(request, user)
                    return redirect(home_view)
                except IntegrityError:
                    return render(request, 'Users/register.html', {
                        'message': "",
                        "Present": True

                    })
            else:
                return render(request, 'Users/register.html', {
                    'message': "Passwords Do not Match",
                    "Present": False
                })
        else:
            return render(request, 'Users/register.html', {
                'message': "Invalid Form Data",
                "Present": False
            })


@login_required
def logout_view(request):
    logout(request)
    return redirect(landing_view)
