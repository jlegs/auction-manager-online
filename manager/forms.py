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

    # I dont think these two things are rquired to make the fields optional.
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.filter(year=lambda: datetime.datetime.now().year), required=False)

    class Meta:
        model = AuctionItem
        fields = ['description', 'date_received', 'retail_value', 'selling_price', 'starting_value', 'increment_amount', 'winning_bid_number', 'invoice']

class InvoiceForm(forms.ModelForm):

    items = forms.ModelChoiceField(queryset=AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year), required=False)
    remove_items = forms.ModelChoiceField(queryset=AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year), required=False)

    class Meta:
        model = Invoice
        fields = ['bill_to', 'paid_for_by', 'total_amount', 'items', 'invoice_date', 'paid', 'payment_type']


class TableInvoiceDetailForm(forms.Form):
    CHOICES = [(attendee.table_assignment, attendee.table_assignment) for attendee in Attendee.objects.filter(table_assignment__isnull=False)]

#    table_assignment = ChoiceField(queryset=Invoice.objects.filter(bill_to__isnull=False).order_by('bill_to__table_assignment'))
    table_assignment = forms.ChoiceField(choices=list(CHOICES))

    class Meta:
        model = Invoice
        fields = []



