from django.contrib import admin
from manager.models.attendee import Attendee
from manager.models.auction_item import AuctionItem
from manager.models.invoice import Invoice

# Register your models here.

admin.site.register(Attendee)
admin.site.register(AuctionItem)
admin.site.register(Invoice)

