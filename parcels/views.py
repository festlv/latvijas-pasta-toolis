# coding=utf-8
from django.shortcuts import render, redirect
from parcels.models import Shipment
from parcels.forms import ShipmentFormSet


def list_parcels(request):
    data = {'title': u'Sūtījumi'}
    parcels = Shipment.objects.user_shipments(request.user)
    data['parcels'] = parcels

    data['active_cat'] = 'list_parcels'
    return render(request, 'parcels/list_parcels.html', data)


def add_parcel(request):
    data = {'title': u'Pievienot sūtījumu'}
    data['active_cat'] = 'add_parcel'

    if request.method == 'POST':
        formset = ShipmentFormSet(
            request.POST, queryset=Shipment.objects.none()
        )
        if formset.is_valid():
            objs = formset.save(commit=False)
            for obj in objs:
                obj.created_user = request.user
                obj.save()
            return redirect('list_parcels')
    else:
        formset = ShipmentFormSet(queryset=Shipment.objects.none())

    data['formset'] = formset
    return render(request, 'parcels/add_parcel.html', data)
