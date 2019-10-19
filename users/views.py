from django.shortcuts import render
from django.contrib.auth.views import LoginView as AuthLoginView
from .forms import LoginForm


class LoginView(AuthLoginView):
    form_class = LoginForm
