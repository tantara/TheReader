from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'Broadcast.views.enter', name='enter'),
    url(r'^reload$', 'Broadcast.views.reload', name='reload'),
    url(r'^(?P<gameId>\w+)$', 'Broadcast.views.show', name='show'),
)
