from django.forms import ModelForm
from manager.models.attendee import Attendee
from manager.models.auction_item import AuctionItem

class AttendeeForm(ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name', 'table_assignment', 'phone', 'email', 'bid_number']


class AuctionItemForm(ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['description', 'date_received', 'retail_value', 'selling_price', 'starting_value', 'increment_amount', 'winning_bid_number', 'invoice']

