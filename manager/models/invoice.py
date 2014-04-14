from django.db import models
from multiselectfield import MultiSelectField


PAYMENT_CHOICES = ((1, 'cash'),
                   (2, 'check'),
                   (3, 'credit card')
                  )


class Invoice(models.Model):
    paid_for_by = models.ForeignKey('Attendee', default=None, related_name='invoices_paid')
    total_amount = models.DecimalField(decimal_places=2, max_digits=30)
    invoice_date = models.DateField()
    paid = models.BooleanField(default=False)
    payment_type = MultiSelectField(choices=PAYMENT_CHOICES)

    class Meta:
        verbose_name_plural = "invoices"
        app_label = 'manager'






