from django.db import models
import datetime




class AuctionItem(models.Model):
    description = models.CharField(max_length=50, blank=True, null=True)
    date_received = models.DateField(blank=True, null=True)
    retail_value = models.DecimalField(decimal_places=2, max_digits=30,blank=True, null=True)
    selling_price = models.DecimalField(decimal_places=2, max_digits=30, blank=True, null=True)
    starting_value = models.DecimalField(decimal_places=2, max_digits=30, blank=True, null=True)
    increment_amount = models.DecimalField(decimal_places=2, max_digits=30, blank=True, null=True)
    winning_bid_number = models.ForeignKey('BidNumber', default=None, related_name='items_won', blank=True, null=True)
    invoice = models.OneToOneField('Invoice', default=None, related_name='item', blank=True, null=True)
    year = models.IntegerField(default=lambda: datetime.datetime.now().year, editable=False)

    class Meta:
        verbose_name_plural = "auction items"
        app_label = 'manager'





