from django.db import models
import datetime

class Attendee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    table_assignment = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    bid_number = models.IntegerField(max_length=3)
    year = models.IntegerField(default=lambda: datetime.datetime.now().year, editable=False)



    class Meta:
        verbose_name_plural = "attendees"
        app_label = 'manager'

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class BidNumber(models.Model):
    bid_number = models.IntegerField()

    class Meta:
        verbose_name_plural = "bid numbers"
        app_label = 'manager'
