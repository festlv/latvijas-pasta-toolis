from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'tracker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('parcels.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('lp_registration.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),

)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
