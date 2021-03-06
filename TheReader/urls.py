from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'TheReader.views.home', name='home'),
    url(r'^about$', 'TheReader.views.about', name='about'),
    url(r'^contact$', 'TheReader.views.contact', name='contact'),
    url(r'^broadcast/', include('Broadcast.urls')),
    # url(r'^TheReader/', include('TheReader.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
		)

if settings.DEBUG:
	urlpatterns += patterns('django.contrib.staticfiles.views',
			url(r'^static/(?P<path>.*)$', 'serve'),
				)

#if settings.DEBUG:
#	urlpatterns += patterns('',
#			(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#				)
