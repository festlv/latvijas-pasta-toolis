# coding=utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
import django.contrib.auth
from django.views.generic.base import View
from registration.backends.simple.views import RegistrationView
from registration.signals import user_registered
from lp_registration.forms import LPRegistrationForm, LoginForm


class LPRegistrationView(RegistrationView):
    form_class = LPRegistrationForm

    def get_success_url(self, request, user):
        return reverse('list_parcels')

    def get_context_data(self, *args, **kwargs):
        data = super(LPRegistrationView, self) \
            .get_context_data(*args, **kwargs)

        data['login_form'] = LoginForm()
        data['active_cat'] = 'register'
        data['title'] = 'Autentifikācija'
        return data


class LogoutView(View):
    def get(self, request):
        django.contrib.auth.logout(request)
        messages.add_message(
            request, messages.SUCCESS, u"Atslēgšanās veiksmīga")
        return redirect('index')


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = django.contrib.auth.authenticate(**form.cleaned_data)
            if user:
                django.contrib.auth.login(request, user)
                return redirect('list_parcels')
        messages.add_message(
            request, messages.ERROR, u"E-pasts vai parole nepareiza")
        return redirect("registration_register")


def post_register(sender, **kwargs):
    messages.add_message(
        kwargs['request'], messages.SUCCESS, u"Reģistrācija veiksmīga")

user_registered.connect(post_register)

