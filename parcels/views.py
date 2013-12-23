# coding=utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from parcels.models import Shipment
from parcels.forms import ShipmentFormSet, ShipmentEditForm
from django.contrib import messages


@login_required
def list_parcels(request):
    data = {'title': u'Sūtījumi'}
    parcels = Shipment.objects.user_shipments(request.user)
    data['parcels'] = parcels

    data['active_cat'] = 'list_parcels'
    return render(request, 'parcels/list_parcels.html', data)


def index(request):
    data = {'active_cat': 'index', 'title': u'Par pasts.wot.lv'}
    return render(request, 'index.html', data)


@login_required
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
                obj.update()
            return redirect('list_parcels')
    else:
        formset = ShipmentFormSet(queryset=Shipment.objects.none())

    data['formset'] = formset
    return render(request, 'parcels/add_parcel.html', data)


@login_required
def search_parcels(request):
    data = {'title': u'Meklēšana'}
    search_term = request.GET.get('q')

    parcels = Shipment.objects.search_shipments(request.user, search_term)
    data['parcels'] = parcels
    return render(request, 'parcels/list_parcels.html', data)


@login_required
def shipment_info(request, shipment_id):
    parcel = get_object_or_404(
        Shipment, created_user=request.user, pk=shipment_id
    )

    data = {'title': u"Informācija par sūtījumu",
            'parcel': parcel}

    return render(request, 'parcels/single_parcel.html', data)


@login_required
def shipment_edit(request, shipment_id):
    parcel = get_object_or_404(
        Shipment, created_user=request.user, pk=shipment_id
    )
    if request.method == 'POST':
        if 'delete' in request.POST:
            parcel.delete()
            messages.add_message(
                request, messages.SUCCESS, u"Sūtījums ir izdzēsts")
            return redirect('list_parcels')
        else:
            form = ShipmentEditForm(instance=parcel, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(
                    request, messages.SUCCESS, u"Sūtījums izlabots")
                return redirect("single_shipment", shipment_id=parcel.pk)

    else:
        form = ShipmentEditForm(instance=parcel)

    data = {'form': form, 'parcel': parcel, 'title': u"Labot/dzēst sūtījumu"}
    return render(request, 'parcels/edit_parcel.html', data)
