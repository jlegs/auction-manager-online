from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login, logout as django_logout
from manager.models.attendee import Attendee, BidNumber
from manager.models.invoice import Invoice
from manager.models.auction_item import AuctionItem
from manager.forms import AttendeeForm
import datetime


def add(request):
    form = AttendeeForm()
    if request.POST:
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            context = {'attendee': attendee,
                       }
            return redirect('attendee_list')

    context = {'form': form,
               }
    return render(request, 'add.html', context)

def info(request, id):
    attendee = Attendee.objects.get(id=id)
    context = {'attendee': attendee,
               'id': id,
               }
    return render(request, 'info.html', context)


def list(request):
    attendees = Attendee.objects.filter(year=lambda: datetime.datetime.now().year)
    context = {'attendees': attendees,
               }
    return render(request, 'attendee_list.html', context)
