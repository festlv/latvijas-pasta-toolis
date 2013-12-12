# urls.py

from django.conf.urls import patterns, url
from lp_registration.views import LPRegistrationView, LogoutView, LoginView

urlpatterns = patterns('',

    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    (r'^register/', LPRegistrationView.as_view()),
    )
