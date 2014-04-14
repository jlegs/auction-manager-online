from django.db import models

class Attendee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    table_assignment = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "attendees"
        app_label = 'manager'


class BidNumber(models.Model):
    bid_number = models.IntegerField()

    class Meta:
        verbose_name_plural = "bid numbers"
        app_label = 'manager'
