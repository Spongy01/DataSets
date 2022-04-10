from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.db import connection, IntegrityError, transaction
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import LoginForm, RegisterForm, CreateFolderForm, CreateTableForm
from .tokens import account_activation_token

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
                    user = CustomUser.objects.create_user(email=email, password=pass1, username=username,
                                                          is_active=False)

                    current_site = get_current_site(request)
                    mail_subject = "Activate Your Account"
                    message = render_to_string('Users/support/activate_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })

                    to_email = email
                    email = EmailMessage(mail_subject, message, to=[to_email])

                    email.send()


                    return render(request, 'Users/register.html',{
                        'message': "Check email for verification",
                        'Present':False,
                    })

                    # login(request, user)
                    # return redirect(home_view)
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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) :
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        login(request, user)

        return redirect(home_view)

    else:
        return HttpResponse("Invalid Link")

