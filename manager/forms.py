from django.forms import ModelForm
from manager.models.attendee import Attendee

# Create the form class.
class AttendeeForm(ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name', 'table_assignment', 'phone', 'email', 'bid_number']