# coding=utf-8
from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from parcels.models import Shipment
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe


class DivErrorList(ErrorList):
    def __unicode__(self):
        return mark_safe(self.as_divs())

    def as_divs(self):
        if not self:
            return u''
        return u''.join([
            u'<div class="alert alert-danger">%s</div>' % e for e in self
        ])


class ShipmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = DivErrorList
        return super(ShipmentForm, self).__init__(*args, **kwargs)

    tracking_number = forms.CharField(
        label='Sūtījuma numurs', required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Sūtījuma numurs',
                'class': 'form-control shipment-no'
            }
        )
    )
    comment = forms.CharField(
        label='Komentārs', required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Komentārs',
                'class': 'form-control comment'
            }
        )
    )

    class Meta:
        model = Shipment
        fields = ['tracking_number', 'comment']

ShipmentFormSet = modelformset_factory(Shipment, form=ShipmentForm, extra=5)
