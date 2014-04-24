import datetime
from django import forms
from manager.models.attendee import Attendee
from manager.models.auction_item import AuctionItem
from manager.models.invoice import Invoice

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name', 'table_assignment', 'phone', 'email', 'bid_number']


class AuctionItemForm(forms.ModelForm):
    # I dont think this is rquired to make the fields optional.
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.filter(year=lambda: datetime.datetime.now().year), required=False)

    class Meta:
        model = AuctionItem
        fields = ['description', 'date_received', 'retail_value', 'selling_price', 'starting_value', 'increment_amount', 'winning_bid_number', 'invoice']

class InvoiceForm(forms.ModelForm):
    items = forms.ModelChoiceField(queryset=AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year).filter(invoice__isnull=True), required=False)
    remove_items = forms.ModelChoiceField(queryset=AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year), required=False)

    class Meta:
        model = Invoice
        fields = ['attendee', 'paid_for_by', 'items', 'invoice_date', 'payment_type']


class TableInvoiceDetailForm(forms.Form):
    CHOICES = {attendee.table_assignment: attendee.table_assignment for attendee in Attendee.objects.all()}

    table_assignment = forms.ChoiceField(choices=CHOICES.iteritems())
    class Meta:
        model = Invoice
        fields = []

class TableAttendeeDetailForm(forms.Form):
    CHOICES = {attendee.table_assignment: attendee.table_assignment for attendee in Attendee.objects.all()}

    table_assignment = forms.ChoiceField(choices=CHOICES.iteritems())
    class Meta:
        model = Attendee
        fields = []


class BidderInvoiceForm(forms.Form):
    bid_number = forms.IntegerField(required=False)
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)

