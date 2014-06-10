import datetime
from django import forms
from manager.models.attendee import Attendee
from manager.models.auction_item import AuctionItem
from manager.models.invoice import Invoice, MergedInvoice
from django_select2 import *

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name', 'table_assignment', 'phone', 'email', 'bid_number']


class AuctionItemForm(forms.ModelForm):
    # I dont think this is rquired to make the fields optional.
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.filter(year=lambda: datetime.datetime.now().year), required=False)

    class Meta:
        model = AuctionItem
        fields = ['description', 'date_received', 'retail_value', 'selling_price', 'starting_value', 'increment_amount', 'winning_bid_number', 'invoice', 'item_number']

class InvoiceForm(forms.ModelForm):
    items = forms.ModelChoiceField(queryset=AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year).filter(invoice__isnull=True), required=False)
    remove_items = forms.ModelChoiceField(queryset=AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year), required=False)

    class Meta:
        model = Invoice
        fields = ['attendee', 'paid_for_by', 'items', 'invoice_date', 'payment_type']


class TableSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('CHOICES')
        super(TableSelectForm, self).__init__(*args, **kwargs)
        self.fields['table_assignment'] = forms.ChoiceField(choices=choices)

#    CHOICES = {attendee.table_assignment: attendee.table_assignment for attendee in Attendee.objects.all()}

#    table_assignment = forms.ChoiceField(choices=CHOICES.iteritems())
#    class Meta:
#        model = Invoice
#        fields = []

class ItemSearchForm(forms.Form):
    item_number = forms.IntegerField()

class YearForm(forms.Form):
    year = forms.IntegerField()

class MergedInvoiceEditForm(forms.ModelForm):
    paid_for_by = forms.CharField(required=False)
    payment_type = 'pi'

    class Meta:
        model = MergedInvoice
        fields = ['paid_for_by', 'payment_type']


queryset = Invoice.objects.filter(year=lambda: datetime.datetime.now().year)
class TableMergeForm(forms.Form):
    invoices = ModelSelect2MultipleField(queryset=queryset)
#    invoice_two = ModelSelect2Field(queryset=queryset)

    # Kinda a bad way to set the styling on these inputs, but the right way to do it is a bit more complicated. TODO: fix this
    def __init__(self, *args, **kwargs):
        super(TableMergeForm, self).__init__(*args, **kwargs)
        self.fields['invoices'].widget.attrs['style'] = 'width: 500;'
#        self.fields['invoice_one'].widget.attrs['style'] = 'width: 500;'


class BidderInvoiceForm(forms.Form):
    bid_number = forms.IntegerField(required=False)
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)

