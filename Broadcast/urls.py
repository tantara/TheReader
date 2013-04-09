from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'Broadcast.views.show', name='show'),
    url(r'^reload$', 'Broadcast.views.reload', name='reload')
)
