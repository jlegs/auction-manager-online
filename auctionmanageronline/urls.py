from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'manager.views.home.home', name='home'),
    url(r'^login/$', 'manager.views.home.login', name='login'),
    url(r'^logout/$', 'manager.views.home.logout', name='logout'),


    url('^attendee/add/$', 'manager.views.attendee.add', name='add_attendee'),
    url('^attendee/(\d+)$', 'manager.views.attendee.info', name='attendee_info'),
    url('^attendee/all$', 'manager.views.attendee.list', name='attendee_list'),

    url(r'^admin/', include(admin.site.urls)),
)
