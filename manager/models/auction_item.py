from decimal import Decimal
from django.db import models
import datetime




class AuctionItem(models.Model):
    description = models.CharField(max_length=50, blank=True)
    date_received = models.DateField(default=lambda: datetime.datetime.now(), blank=True, null=True)
    invoice = models.ForeignKey('Invoice', related_name='items', default=None, blank=True, null=True)
    retail_value = models.DecimalField(decimal_places=2, max_digits=30)
    selling_price = models.DecimalField(decimal_places=2, max_digits=30, default=Decimal('0.00'), blank=True, null=True)
    starting_value = models.DecimalField(decimal_places=2, max_digits=30)
    increment_amount = models.DecimalField(decimal_places=2, max_digits=30)
    winning_bid_number = models.IntegerField(default=None, blank=True, null=True)
    year = models.IntegerField(default=lambda: datetime.datetime.now().year, editable=False)
    item_number = models.IntegerField(default=None)

    class Meta:
        verbose_name_plural = "auction items"
        app_label = 'manager'

    def __unicode__(self):
        return self.description





