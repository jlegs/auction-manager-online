from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'manager.views.home.home', name='home'),
    url(r'^login/$', 'manager.views.home.login', name='login'),
    url(r'^logout/$', 'manager.views.home.logout', name='logout'),


    url('^attendee/add/$', 'manager.views.attendee.create', name='add_attendee'),
    url('^attendee/(\d+)$', 'manager.views.attendee.info', name='attendee_info'),
    url('^attendee/update/(\d+)$', 'manager.views.attendee.update', name='update_attendee'),
    url('^attendee/all$', 'manager.views.attendee.list', name='attendee_list'),
    url('^attendee/delete/(\d+)$', 'manager.views.attendee.delete', name='delete_attendee'),


    url('^item/add/$', 'manager.views.auction_item.create', name='add_item'),
    url('^item/(\d+)$', 'manager.views.auction_item.info', name='item_info'),
    url('^item/update/(\d+)$', 'manager.views.auction_item.update', name='update_item'),
    url('^item/all$', 'manager.views.auction_item.list', name='item_list'),
    url('^item/delete/(\d+)$', 'manager.views.auction_item.delete', name='delete_item'),


    url(r'^admin/', include(admin.site.urls)),
)
