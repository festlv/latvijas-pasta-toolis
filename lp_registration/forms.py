from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationFormUniqueEmail


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class LPRegistrationForm(RegistrationFormUniqueEmail, BootstrapForm):

    username = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean(self):
        data = super(LPRegistrationForm, self).clean()
        if 'email' in data:
            found_free = False

            username = data['email'].split('@')[0]
            i = 0
            while not found_free:
                test_name = "%s-%d" % (username, i)
                if User.objects.filter(
                    username__iexact=test_name
                ).count() == 0:
                    username = test_name
                    break
                i += 1

            data['username'] = username

        return data


class LoginForm(BootstrapForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
