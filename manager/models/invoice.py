from django.db import models
from multiselectfield import MultiSelectField
import datetime


PAYMENT_CHOICES = ((1, 'cash'),
                   (2, 'check'),
                   (3, 'credit card')
                   )

# TODO, make sure payment type choices field works
class Invoice(models.Model):
    paid_for_by = models.ForeignKey('Attendee', default=None, related_name='invoices_paid', blank=True, null=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=30, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    paid = models.BooleanField(default=False, blank=True)
    payment_type = models.CharField(max_length=3, choices=PAYMENT_CHOICES, blank=True, null=True)
    year = models.IntegerField(default=lambda: datetime.datetime.now().year, editable=False)


    class Meta:
        verbose_name_plural = "invoices"
        app_label = 'manager'






