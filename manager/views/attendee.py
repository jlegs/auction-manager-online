from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login, logout as django_logout
from manager.models.attendee import Attendee
from manager.models.invoice import Invoice
from manager.models.auction_item import AuctionItem
from manager.forms import AttendeeForm
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def create(request):
    ''' creates a new attendee for the current year's auction.
    '''
    if request.POST:
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            invoice = Invoice(total_amount=0)
            invoice.attendee = attendee
            invoice.save()
            messages.add_message(request, messages.SUCCESS, 'New Attendee Added. Invoice added and associated with attendee.')
            return redirect('attendee_list')
        else:
            if len(Attendee.objects.filter(year=lambda: datetime.datetime.now().year)) > 0:
                latest = Attendee.objects.latest('bid_number')
                bid_number = latest.bid_number + 1
            context = {'form': form,
                       'bid_number': bid_number,
                       'table_assignment': form.cleaned_data['table_assignment']}
            return render(request, 'attendee/add.html', context)
    else:
        form = AttendeeForm()
        # Check to see if there are attendees for this year's auction. If there are, set the default bid number
        # to one more than the highest bid number. If no attendees, set bid number to 1.
        if len(Attendee.objects.filter(year=lambda: datetime.datetime.now().year)) > 0:
            latest = Attendee.objects.latest('bid_number')
            bid_number = latest.bid_number + 1
        else:
            bid_number = 1
        context = {'form': form,
                   'bid_number': bid_number,
                   }
        return render(request, 'attendee/add.html', context)


def update(request, id):
    ''' Updates an attendee record
    '''
    attendee = get_object_or_404(Attendee, id=id)

    if request.POST:
        form = AttendeeForm(request.POST, instance=attendee)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Attendee Information updated for %s' % (attendee.first_name + " " + attendee.last_name))
            return redirect('attendee_list')
        else:
            return redirect('attendee_info', id)
    else:
        form = AttendeeForm(instance=attendee)
        context = {'attendee': attendee,
                   'form': form,
                   }

    return render(request, 'attendee/update.html', context)



def info(request, id):
    ''' Unimplemented
    '''
    attendee = Attendee.objects.get(id=id)
    return render(request, 'attendee/info.html', {'attendee': attendee})


def list(request):
    ''' Get a list of all attendees for the current year's auction.
    '''
    attendees = Attendee.objects.filter(year=lambda: datetime.datetime.now().year)
    context = {'attendees': attendees,
               }
    return render(request, 'attendee/attendee_list.html', context)

def confirm_delete(request, id):
    return redirect('home')


def delete(request, id):
    attendee = Attendee.objects.get(id=id)
    attendee.delete()
    return redirect('attendee_list')


def table_list(request):
    attendees = Attendee.objects.all().order_by('table_assignment')
    context = {'attendees': attendees}
    return render(request, 'attendee/table_list.html', context)



