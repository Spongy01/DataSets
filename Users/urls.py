
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/landing/'),),
    path('landing/', views.landing_view, name="landing page"),
    path('login/', views.login_view, name="login page"),
    path('register/', views.register_view, name="register page"),
    path('logout/', views.logout_view, name="logout"),
]