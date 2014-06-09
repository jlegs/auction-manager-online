from django.db import models
import datetime


PAYMENT_CHOICES = (('cash', 'cash'),
                   ('check', 'check'),
                   ('credit', 'credit card')
                   )

class Invoice(models.Model):
    '''
    This provides basic data for invoices. Add items to the invoice by
    using invoice.items.add(item). Remove them using invoice.items.remove(item).
    Deleting an invoice will delete items associated with it. This
    is prevented in the view
    '''
    attendee = models.OneToOneField('Attendee',
                                    default=None,
                                    related_name='invoice',
                                    blank=True,
                                    null=True)
    paid_for_by = models.ForeignKey('Attendee',
                                    default=None,
                                    related_name='invoices_paid',
                                    blank=True,
                                    null=True)
    invoice_date = models.DateField(default=lambda: datetime.datetime.now(),
                                    blank=True,
                                    null=True)
    payment_type = models.CharField(max_length=50,
                                    choices=PAYMENT_CHOICES,
                                    blank=True,
                                    null=True)
    year = models.IntegerField(default=lambda: datetime.datetime.now().year,
                               editable=False)
    merged_invoice = models.ForeignKey('MergedInvoice',
                                       default=None,
                                       related_name="invoices",
                                       blank=True,
                                       null=True)


    class Meta:
        verbose_name_plural = "invoices"
        app_label = 'manager'

    def __unicode__(self):
        return "Invoice for: %s" % self.attendee

    def add_item_value(self, item):
        '''
        legacy code
        '''
        self.total_amount += item.selling_price
        self.save()

    def remove_item_value(self, item):
        '''
        legacy code
        '''
        self.total_amount -= item.selling_price
        self.save()

    def set_total(self):
        '''
        legacy code -- used to set the total_amount attribute
        '''
        self.total_amount = 0
        for item in self.items.all():
            if item.selling_price:
                self.total_amount += item.selling_price
            else:
                pass
        return self.total_amount

    @property
    def total_amount(self):
        '''
        Dynamically determines the invoice's total. Conveneient because you
        don't need to set an attribute.
        '''
        total = 0
        for item in self.items.all():
            if item.selling_price:
                total += item.selling_price
            else:
                pass
        return total



class MergedInvoice(models.Model):
    '''
    Merged invoice -- combining invoices creates an instance of this class.
    It will leave original invoices intact. Setting the paid_for_by and
    payment_type attributes on this instance will set those attributes on the original
    invoices as well. That's the only change allowable on invoices from merged invoices.
    '''
    paid_for_by = models.ForeignKey('Attendee', default=None,
                                    related_name='merged_invoices_paid',
                                    blank=True,
                                    null=True)
    invoice_date = models.DateField(default=lambda: datetime.datetime.now(),
                                    blank=True,
                                    null=True)
    payment_type = models.CharField(max_length=50,
                                    choices=PAYMENT_CHOICES,
                                    blank=True,
                                    null=True)
    year = models.IntegerField(default=lambda: datetime.datetime.now().year,
                               editable=False)


    class Meta:
        verbose_name_plural = "merged_invoices"
        app_label = 'manager'

    def __unicode__(self):
        return "Merged Invoice"

    @property
    def total_amount(self):
        '''
        get the amount owed for the invoice
        '''
        total = 0
        for invoice in self.invoices.all():
            for item in invoice.items.all():
                if item.selling_price:
                    total += item.selling_price
                else:
                    pass
        return total


