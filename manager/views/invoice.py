from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login, logout as django_logout
from manager.models.auction_item import AuctionItem
from manager.models.attendee import Attendee
from manager.models.invoice import Invoice, MergedInvoice
from manager.models.auction_item import AuctionItem
from manager.forms import InvoiceForm, TableSelectForm, BidderInvoiceForm, AttendeeForm, TableMergeForm, YearForm
import datetime
from django.contrib import messages
from collections import OrderedDict


def create(request):
    ''' creates a new invoice for the current year's auction.
    '''
    if request.POST:
        form = InvoiceForm(request.POST)
        if form.is_valid():
            new_invoice = form.save()
            if form.cleaned_data['items']:
                item = AuctionItem.objects.get(id=form.cleaned_data['items'].id)
                new_invoice.items.add(item)
                new_invoice.save()
            messages.add_message(request, messages.SUCCESS, 'New Invoice Saved')
            return redirect('invoice_list')
        else:
            context = {'form': form}
            return render(request, 'invoice/add.html', context)
    else:
        form = InvoiceForm()
        context = {'form': form,
                   }
        return render(request, 'invoice/add.html', context)


def update(request, id):
    ''' Updates an auction item record
    '''
    invoice = get_object_or_404(Invoice, id=id)

    if request.POST:
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            if form.cleaned_data['items']:
                item = AuctionItem.objects.get(id=form.cleaned_data['items'].id)
                invoice.items.add(item)
                messages.add_message(request, messages.SUCCESS, 'Item added to invoice.')
            elif form.cleaned_data['remove_items']:
                item = AuctionItem.objects.get(id=form.cleaned_data['remove_items'].id)
                invoice.items.remove(item)
                messages.add_message(request, messages.SUCCESS, 'Item removed from invoice.')
            #invoice.set_total()
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Invoice updated.')
            return redirect('invoice_list')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong, likely some kind of form validation.')
            return render(request, 'invoice/update.html', {'form': form})
    else:
        form = InvoiceForm(instance=invoice)
        form.fields['remove_items'].queryset = AuctionItem.objects.filter(invoice=invoice)

        context = {'invoice': invoice,
                   'form': form,
                   }

    return render(request, 'invoice/update.html', context)



def info(request, id):
    ''' Deletes an invoice
    '''
    invoice = get_object_or_404(Invoice, id=id)
    ## Call save() here because it will set the invoice total to the correct amount if it's wrong, which sometimes
    ## happens when disassociating an item with an invoice, or associating an item with a different invoice
    invoice.save()
    return render(request, 'invoice/info.html', {'invoice': invoice})


def list(request):
    ''' Get a list of all auction items for the current year's auction.
    '''
    invoices = Invoice.objects.filter(year=lambda: datetime.datetime.now().year)
    context = {'invoices': invoices,
               }
    return render(request, 'invoice/invoice_list.html', context)

def confirm_delete(request, id):
    return redirect('home')


def delete(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    if invoice.items.all():
        messages.add_message(request, messages.WARNING, 'Unable to delete invoices that have items associated with '
                                                        'them.')
        return redirect('invoice_list')
    else:
        invoice.delete()
    return redirect('invoice_list')


def table_list(request):
    invoices = Invoice.objects.filter(attendee__isnull=False).order_by('attendee__table_assignment')
    context = {'invoices': invoices}
    return render(request, 'invoice/invoice_list.html', context)

def table_invoices_detail(request):
    invoices = Invoice.objects.filter(attendee__isnull=False).order_by('attendee__table_assignment')
    context = {'invoices': invoices}
    return render(request, 'invoice/table_invoices_detail.html', context)

def table_invoice_detail(request):
    choices = set([(a.table_assignment, a.table_assignment) for a in Attendee.objects.filter(year=datetime.datetime.now().year)])

    if request.POST:
        form = TableSelectForm(request.POST, CHOICES=choices)
        if form.is_valid():
            invoices = Invoice.objects.filter(attendee__isnull=False).filter(attendee__table_assignment=form.cleaned_data['table_assignment'])
            context = {'invoices': invoices,
                       'form': form,
                       'table': invoices[0].attendee.table_assignment,
                       }
        else:
            return redirect('invoice_list')
    else:
        form = TableSelectForm(CHOICES=choices)
#        form.fields['table_assignment'].queryset = {attendee.table_assignment: attendee.table_assignment for attendee in Attendee.objects.filter(year=lambda: datetime.datetime.now().year)}
        context = {'form': form}
    return render(request, 'invoice/table_invoice_detail.html', context)




def merge_invoices(request):
    if request.POST:
        form = TableMergeForm(request.POST)
        if form.is_valid():
            invoices = form.cleaned_data['invoices']
            new_invoice = Invoice()
            for invoice in invoices:
                for item in invoice.items.all():
                    new_invoice.items.add(item)
                    new_invoice.save()
            context = {'form': form,
                       'new_invoice': new_invoice,
            }
            return render(request, 'invoice/merge.html', context)
        else:
            return redirect('merge_invoices')
    else:
        form = TableMergeForm()
        context = {'form': form}
    return render(request, 'invoice/merge.html', context)




def merged_invoice(request, id):
    invoice = MergedInvoice.objects.get(id=id)
    context = {'invoice': invoice}
    return render(request, 'invoice/merged_invoice.html', context)


def past_invoices(request):
    ''' Get a list of all auction items for the a past year's auction.
    '''
    context = {}
    if request.POST:
        form = YearForm(request.POST)
        if form.is_valid():
            invoices = Invoice.objects.filter(year=form.cleaned_data['year'])
            context['invoices'] = invoices
            context['year'] = form.cleaned_data['year']
        else:
            context['errors'] = form.errors
            context['form'] = form
        return render(request, 'invoice/invoice_list.html', context)
    else:
        form = YearForm()
        context['form'] = form
    return render(request, 'invoice/invoice_list.html', context)



def bidder_invoice(request):
    context = {}
    if request.POST:
        form = BidderInvoiceForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['bid_number']:
                attendee = Attendee.objects.get(bid_number=form.cleaned_data['bid_number'])
                invoice = Invoice.objects.get(attendee=attendee)
                context['invoice'] = invoice
            # The next four lines dont work. need to implement a better form for this
            if form.cleaned_data['last_name']:
                attendees = Attendee.objects.filter(last_name=form.cleaned_data['last_name'])
                invoices = Invoice.objects.filter(attendee__in=attendees)
                context.update({'invoices': invoices})
            if form.cleaned_data['first_name']:
                attendees = Attendee.objects.filter(first_name=form.cleaned_data['first_name'])
                invoices = Invoice.objects.filter(attendee__in=attendees)
                context.update({'invoices': invoices})
            context['form'] = form
        else:
            context['errors'] = form.errors
            context['form'] = form
        return render(request, 'invoice/bidder_invoice.html', context)
    else:
        form = BidderInvoiceForm()
#        form.fields['table_assignment'].queryset = {attendee.table_assignment: attendee.table_assignment for attendee in Attendee.objects.filter(year=lambda: datetime.datetime.now().year)}
        context = {'form': form}
    return render(request, 'invoice/bidder_invoice.html', context)




