from django.db import models
import datetime




class AuctionItem(models.Model):
    description = models.CharField(max_length=50)
    date_received = models.DateField()
    retail_value = models.DecimalField(decimal_places=2, max_digits=30)
    selling_price = models.DecimalField(decimal_places=2, max_digits=30)
    starting_value = models.DecimalField(decimal_places=2, max_digits=30)
    increment_amount = models.DecimalField(decimal_places=2, max_digits=30)
    winning_bid_number = models.ForeignKey('BidNumber', default=None, related_name='items_won', blank=True, null=True)
    invoice = models.OneToOneField('Invoice', default=None, related_name='item')
    year = models.IntegerField(default=lambda: datetime.datetime.now().year, editable=False)

    class Meta:
        verbose_name_plural = "auction items"
        app_label = 'manager'





