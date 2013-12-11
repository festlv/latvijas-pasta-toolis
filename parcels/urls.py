from django.conf.urls import patterns, url

urlpatterns = patterns('parcels.views',
    url(r'^$', 'list_parcels'),
    url(r'^list/$', 'list_parcels', name='list_parcels'),
    url(r'^add_shipment/$', 'add_parcel'),
)
