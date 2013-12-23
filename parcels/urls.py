from django.conf.urls import patterns, url

urlpatterns = patterns('parcels.views',
    url(r'^$', 'index', name='index'),
    url(r'^list/$', 'list_parcels', name='list_parcels'),
    url(r'^add_shipment/$', 'add_parcel'),
    url(r'^shipment/(?P<shipment_id>\d+)/$', 'shipment_info', name="single_shipment"),
    url(r'^search/$', 'search_parcels', name='search_parcels'),
)
