from decimal import Decimal
from django.db import models
from multiselectfield import MultiSelectField
import datetime


PAYMENT_CHOICES = (('cash', 'cash'),
                   ('check', 'check'),
                   ('credit', 'credit card')
                   )

# TODO, make sure payment type choices field works
class Invoice(models.Model):
    bill_to = models.ForeignKey('Attendee', default=None, related_name='invoices', blank=True, null=True)
    paid_for_by = models.ForeignKey('Attendee', default=None, related_name='invoices_paid', blank=True, null=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=30, default=Decimal('0.00'), blank=True, null=True)
    invoice_date = models.DateField(default=lambda: datetime.datetime.now(), blank=True, null=True)
    paid = models.BooleanField(default=False, blank=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES, blank=True, null=True)
    year = models.IntegerField(default=lambda: datetime.datetime.now().year, editable=False)


    class Meta:
        verbose_name_plural = "invoices"
        app_label = 'manager'

    def __unicode__(self):
        return "Invoice for: %s" % self.bill_to

    def add_item_value(self, item):
        self.total_amount += item.selling_price
        self.save()

    def remove_item_value(self, item):
        self.total_amount -= item.selling_price
        self.save()

    def set_total(self):
        self.total_amount = 0
        for item in self.items.all():
            if item.selling_price:
                self.total_amount += item.selling_price
            else:
                pass
        return self.total_amount


