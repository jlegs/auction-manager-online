from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login, logout as django_logout
from manager.models.attendee import Attendee
from manager.models.invoice import Invoice
from manager.models.auction_item import AuctionItem
from manager.forms import AttendeeForm, TableSelectForm, YearForm
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required
def create(request):
    ''' creates a new attendee for the current year's auction.
    '''
    if request.POST:
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            attendee.create_invoice()
            messages.add_message(request, messages.SUCCESS, 'New Attendee Added. Invoice added and associated with attendee.')
            return redirect('attendee_list')
        else:
            if len(Attendee.objects.filter(year=lambda: datetime.datetime.now().year)) > 0:
                latest_attendee = Attendee.objects.latest('bid_number')
                bid_number = latest_attendee.bid_number + 1
            context = {'form': form,
                       'bid_number': bid_number,
                       'table_assignment': form.cleaned_data['table_assignment']}
            return render(request, 'attendee/add.html', context)
    else:
        form = AttendeeForm()
        # Check to see if there are attendees for this year's auction. If there are, set the default bid number
        # to one more than the highest bid number. If no attendees, set bid number to 1.
        if len(Attendee.objects.filter(year=lambda: datetime.datetime.now().year)) > 0:
            latest_attendee = Attendee.objects.latest('bid_number')
            bid_number = latest_attendee.bid_number + 1
        else:
            bid_number = 1
        context = {'form': form,
                   'bid_number': bid_number,
                   }
        return render(request, 'attendee/add.html', context)


@login_required
def update(request, id):
    ''' Updates an attendee record
    '''
    attendee = get_object_or_404(Attendee, id=id)
    # Get current list of bid numbers so we don't accidentally assign one that already exists.
    bid_list = [a.bid_number for a in Attendee.objects.filter(year=lambda: datetime.datetime.now().year).exclude(
        id=attendee.id)]
    if request.POST:
        form = AttendeeForm(request.POST, instance=attendee)
        if form.is_valid():
            if form.cleaned_data['bid_number'] in bid_list:
                messages.add_message(request, messages.WARNING, 'That bid number is already assigned to another guest')
                return redirect('attendee_info', id)
            else:
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



@login_required
def info(request, id):
    ''' Gets info for an attendee
    '''
    attendee = Attendee.objects.get(id=id)
    return render(request, 'attendee/info.html', {'attendee': attendee})


@login_required
def list(request):
    ''' Get a list of all attendees for the current year's auction.
    '''
    attendees = Attendee.objects.filter(year=lambda: datetime.datetime.now().year)
    context = {'attendees': attendees,
               }
    return render(request, 'attendee/attendee_list.html', context)


@login_required
def delete(request, id):
    '''
    deletes an attendee
    '''
    attendee = Attendee.objects.get(id=id)
    attendee.delete()
    return redirect('attendee_list')


@login_required
def table_list(request):
    '''
    orders attendees by table
    '''
    attendees = Attendee.objects.all().order_by('table_assignment')
    context = {'attendees': attendees}
    return render(request, 'attendee/table_list.html', context)

@login_required
def table_attendee_detail(request):
    '''
    View to retrieve all attendees at a certain table
    '''
    choices = set([(a.table_assignment, a.table_assignment) for a in Attendee.objects.filter(year=datetime.datetime.now().year)])

    if request.POST:
        form = TableSelectForm(request.POST, CHOICES=choices)
        if form.is_valid():
            attendees = Attendee.objects.filter(table_assignment=form.cleaned_data['table_assignment'])
            context = {'attendees': attendees,
                       'form': form}
    else:
        form = TableSelectForm(CHOICES=choices)
        context = {'form': form}
    return render(request, 'attendee/table_detail_list.html', context)



@login_required
def past_attendees(request):
    ''' Get a list of all auction items for the a past year's auction.
    '''
    context = {}
    if request.POST:
        form = YearForm(request.POST)
        if form.is_valid():
            attendees = Attendee.objects.filter(year=form.cleaned_data['year'])
            context['attendees'] = attendees
            context['year'] = form.cleaned_data['year']
        else:
            context['errors'] = form.errors
            context['form'] = form
        return render(request, 'attendee/attendee_list.html', context)
    else:
        form = YearForm()
        context['form'] = form
    return render(request, 'attendee/attendee_list.html', context)

