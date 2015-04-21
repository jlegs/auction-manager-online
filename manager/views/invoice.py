from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from manager.models.attendee import Attendee
from manager.models.invoice import Invoice, MergedInvoice
from manager.models.auction_item import AuctionItem
from manager.forms import InvoiceForm, TableSelectForm, BidderInvoiceForm, TableMergeForm, YearForm, MergedInvoiceEditForm
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger('auction')


@login_required
def create(request):
    '''
    creates a new invoice for the current year's auction.
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


@login_required
def update(request, id):
    '''
    Updates an invoice record
    '''
    invoice = get_object_or_404(Invoice, id=id)

    if request.POST:
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            add_item = form.cleaned_data['items']
            remove_item = form.cleaned_data['remove_items']
            invoice.update_invoice(add_item=add_item, remove_item=remove_item)
            messages.add_message(request, messages.SUCCESS, 'Invoice for {} updated.'.format(invoice.attendee.name))
            logger.info('Invoice updated')
            return redirect('invoice_list')
        else:
            messages.add_message(request, messages.WARNING,
                                 'Something went wrong, likely some kind of form validation.')
            logger.error('Something went wrong updating the invoice.')
            return render(request, 'invoice/update.html', {'form': form})
    else:
        form = InvoiceForm(instance=invoice)
        form.fields['remove_items'].queryset = AuctionItem.objects.filter(invoice=invoice)

        context = {'invoice': invoice,
                   'form': form,
                   }

    return render(request, 'invoice/update.html', context)



@login_required
def detail(request, id):
    '''
    gets an invoices details
    '''
    invoice = get_object_or_404(Invoice, id=id)
    ## Call save() here because it will set the invoice total to the correct amount if it's wrong, which sometimes
    ## happens when disassociating an item with an invoice, or associating an item with a different invoice
    invoice.save()
    logger.info('Displaying invoice details')
    return render(request, 'invoice/info.html', {'invoice': invoice})


@login_required
def list(request):
    ''' Get a list of all auction items for the current year's auction.
    '''
    invoices = Invoice.objects.filter(year=lambda: datetime.datetime.now().year)
    logger.info('Displaying list of invoices')
    context = {'invoices': invoices,
               }
    return render(request, 'invoice/invoice_list.html', context)



@login_required
def delete(request, id):
    '''
    deletes an invoice
    '''
    invoice = get_object_or_404(Invoice, id=id)
    if invoice.items.all():
        messages.add_message(request, messages.WARNING, 'Unable to delete invoices that have items associated with '
                                                        'them.')
        logger.error('Error deleting invoice because items still associated with invoice.')
        return redirect('invoice_list')
    else:
        invoice.delete()
        logger.info('Deleting invoice')
    return redirect('invoice_list')


@login_required
def table_list(request):
    '''
    get a list of invoices by table
    '''
    invoices = Invoice.objects.filter(
        attendee__isnull=False).order_by('attendee__table_assignment')
    logger.info('Displaying list of invoices by table')
    context = {'invoices': invoices}
    return render(request, 'invoice/invoice_list.html', context)


@login_required
def unpaid_invoices(request):
    '''
    get a list of unpaid invoices
    '''
    invoices = Invoice.objects.filter(
        attendee__isnull=False).filter(paid_for_by__isnull=True)
    context = {'invoices': invoices}
    return render(request, 'invoice/invoice_list.html', context)



@login_required
def table_invoice_detail(request):
    '''
    get whole invoices grouped by table
    '''
    choices = set([(a.table_assignment, a.table_assignment) for a in Attendee.objects.filter(year=datetime.datetime.now().year)])

    if request.POST:
        form = TableSelectForm(request.POST, CHOICES=choices)
        if form.is_valid():
            invoices = Invoice.objects.filter(attendee__table_assignment=form.cleaned_data['table_assignment']).exclude(items__isnull=True)
            context = {'invoices': invoices,
                       'form': form,
                       'table': form.cleaned_data['table_assignment'],
                       }
            logger.info('Displaying invoices by table.')
            if not invoices:
                messages.add_message(request, messages.INFO, 'No bidders at this table have invoices that need to be billed.')
                logger.error('No bidders at table have invoices that need to be billed.')
        else:
            return redirect('invoice_list')
    else:
        form = TableSelectForm(CHOICES=choices)
        context = {'form': form}
    return render(request, 'invoice/table_invoice_detail.html', context)




@login_required
def merge_invoices(request):
    '''
    create a merged invoice containing two or more regular invoices
    '''
    if request.POST:
        form = TableMergeForm(request.POST)
        if form.is_valid():
            merged_invoices = MergedInvoice.objects.filter(invoices__in=form.cleaned_data['invoices'])
            invoices = form.cleaned_data['invoices']
            if not merged_invoices and len(invoices) > 1:
                new_invoice = MergedInvoice()
                new_invoice.save()
                for invoice in invoices:
                    new_invoice.invoices.add(invoice)
                context = {'form': form,
                           'new_invoice': new_invoice,
                }
                logger.info('Merging invoices {}'.format(new_invoice.invoices.all()))
            else:
                messages.add_message(request, messages.WARNING, 'One of the invoices you tried to merge has already been merged with another, or you have not selected enough invoices to merge.')
                context = {'form': form,
                           }
                logger.error('Merging invoices failed because at least one invoice already belongs to a merged invoice record.')
            return render(request, 'invoice/merge.html', context)
        else:
            logger.error('Invalid merge-invoice form. Redirecting.')
            return redirect('merge_invoices')
    else:
        form = TableMergeForm()
        context = {'form': form}
    return render(request, 'invoice/merge.html', context)


@login_required
def delete_merged_invoice(request, id):
    '''
    delete a merged invoice
    '''
    merged_invoice = get_object_or_404(MergedInvoice, id=id)
    if merged_invoice.invoices.all():
        for invoice in merged_invoice.invoices.all():
            merged_invoice.invoices.remove(invoice)
    merged_invoice.delete()
    logging.info('Deleting merged invoice.')
    return redirect('merged_invoice_list')



@login_required
def merged_invoice_list(request):
    ''' Get a list of all auction items for the current year's auction.
    '''
    merged_invoices = MergedInvoice.objects.filter(year=lambda: datetime.datetime.now().year)
    context = {'merged_invoices': merged_invoices,
               }
    return render(request, 'invoice/merged_invoice_list.html', context)

@login_required
def update_merged_invoice(request, id):
    ''' Updates an auction item record
    '''
    merged_invoice = get_object_or_404(MergedInvoice, id=id)

    if request.POST:
        form = MergedInvoiceEditForm(request.POST, instance=merged_invoice)
        if form.is_valid():

            form.save()
            merged_invoice.update_invoices()
            messages.add_message(request, messages.SUCCESS, 'Invoice updated.')
            logger.info('Updating merged invoice and associated invoices.')
            return redirect('merged_invoice_list')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong, likely some kind of form validation.')
            logger.error('Something went wrong while updating merged invoice.')
            return render(request, 'invoice/merged_invoice_update.html', {'form': form})
    else:
        form = MergedInvoiceEditForm(instance=merged_invoice)

        context = {'invoice': merged_invoice,
                   'form': form,
                   }

    return render(request, 'invoice/merged_invoice_update.html', context)




@login_required
def merged_invoice(request, id):
    '''
    get the details of a merged invoice
    '''
    invoice = MergedInvoice.objects.get(id=id)
    context = {'merged_invoice': invoice}
    return render(request, 'invoice/merged_invoice.html', context)


@login_required
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
            context['' \
                    'errors'] = form.errors
            context['form'] = form
        return render(request, 'invoice/invoice_list.html', context)
    else:
        form = YearForm()
        context['form'] = form
    return render(request, 'invoice/invoice_list.html', context)



@login_required
def bidder_invoice_search(request):
    '''
    search for invoice by bidder name or number
    '''
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
        context = {'form': form}
    return render(request, 'invoice/bidder_invoice.html', context)




