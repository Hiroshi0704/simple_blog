from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import LoginForm

class Login(LoginView):
    form_class = LoginForm
