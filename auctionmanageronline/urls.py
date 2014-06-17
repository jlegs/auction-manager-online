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
    url('^past-attendees$', 'manager.views.attendee.past_attendees', name='past_attendees'),

    url('^item/add/$', 'manager.views.auction_item.create', name='add_item'),
    url('^item/(\d+)$', 'manager.views.auction_item.info', name='item_info'),
    url('^item/update/(\d+)$', 'manager.views.auction_item.update', name='update_item'),
    url('^item/all$', 'manager.views.auction_item.list', name='item_list'),
    url('^item/delete/(\d+)$', 'manager.views.auction_item.delete', name='delete_item'),
    url('^item/search/$', 'manager.views.auction_item.item_search', name='item_search'),
    url('^item/unsold/all$', 'manager.views.auction_item.unsold_item_list', name='unsold_items'),
    url('^past-items$', 'manager.views.auction_item.past_items', name='past_items'),

    url('^invoice/add/$', 'manager.views.invoice.create', name='add_invoice'),
    url('^invoice/(\d+)$', 'manager.views.invoice.info', name='invoice_info'),
    url('^invoice/bidder/(\d+)$', 'manager.views.invoice.bidder_invoice', name='bidder_invoice'),
    url('^invoice/update/(\d+)$', 'manager.views.invoice.update', name='update_invoice'),
    url('^invoice/all$', 'manager.views.invoice.list', name='invoice_list'),
    url('^invoice/delete/(\d+)$', 'manager.views.invoice.delete', name='delete_invoice'),

    url('^invoice/merge/$', 'manager.views.invoice.merge_invoices', name='merge_invoices'),
    url('^merged-invoice/(\d+)$', 'manager.views.invoice.merged_invoice', name='merged_invoice_info'),
    url('^merged-invoice/update/(\d+)$', 'manager.views.invoice.update_merged_invoice', name='update_merged_invoice'),
    url('^merged-invoice/all$', 'manager.views.invoice.merged_invoice_list', name='merged_invoice_list'),
    url('^merged-invoice/delete/(\d+)$', 'manager.views.invoice.delete_merged_invoice', name='delete_merged_invoice'),

    url('^past-invoices$', 'manager.views.invoice.past_invoices', name='past_invoices'),

    url('^attendee/table/all$', 'manager.views.attendee.table_list', name='table_list'),
    url('^attendee/table/detail$', 'manager.views.attendee.table_attendee_detail', name='table_attendee_detail'),
    url('^invoice/table/list/all$', 'manager.views.invoice.table_list', name='table_invoices'),
    url('^invoice/table/detail/$', 'manager.views.invoice.table_invoice_detail', name='table_invoice_detail'),
    url('^invoice/bidder/$', 'manager.views.invoice.bidder_invoice', name='bidder_invoice'),
    url('^invoice/unpaid/$', 'manager.views.invoice.unpaid_invoices', name='unpaid_invoices'),


    url(r'^select2/', include('django_select2.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
