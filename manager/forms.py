import datetime
from django.forms import ModelForm, ModelChoiceField
from manager.models.attendee import Attendee
from manager.models.auction_item import AuctionItem
from manager.models.invoice import Invoice

class AttendeeForm(ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name', 'table_assignment', 'phone', 'email', 'bid_number']


class AuctionItemForm(ModelForm):

    # I dont think these two things are rquired to make the fields optional.
    winning_bid_number = ModelChoiceField(queryset=Attendee.objects.filter(year=lambda: datetime.datetime.now().year), required=False)
    invoice = ModelChoiceField(queryset=Invoice.objects.all(), required=False)

    class Meta:
        model = AuctionItem
        fields = ['description', 'date_received', 'retail_value', 'selling_price', 'starting_value', 'increment_amount', 'winning_bid_number', 'invoice']

class InvoiceForm(ModelForm):



    class Meta:
        model = Invoice
        fields = ['paid_for_by', 'total_amount', 'invoice_date', 'paid', 'payment_type']

