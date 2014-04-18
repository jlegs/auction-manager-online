from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login, logout as django_logout
from manager.models.auction_item import AuctionItem
from manager.models.invoice import Invoice
from manager.models.auction_item import AuctionItem
from manager.forms import InvoiceForm
import datetime
from django.contrib import messages


def create(request):
    ''' creates a new invoice for the current year's auction.
    '''
    if request.POST:
        form = InvoiceForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.add_message(request, messages.SUCCESS, 'New Invoice Saved')
            return redirect('invoice_list')
        else:
            context = {'form': form}
#            return redirect('add_item')
            return render(request, 'invoice/add.html', context)
    else:
        form = InvoiceForm()
        context = {'form': form,
                   }
        return render(request, 'invoice/add.html', context)
    return redirect('invoice_list')


def update(request, id):
    ''' Updates an auction item record
    '''
    item = get_object_or_404(Invoice, id=id)

    if request.POST:
        form = InvoiceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Invoice updated')
            return redirect('invoice_list')
        else:
            return redirect('invoice_info', id)
    else:
        form = InvoiceForm(instance=item)
        context = {'invoice': item,
                   'form': form,
                   }

    return render(request, 'invoice/update.html', context)



def info(request, id):
    ''' Deletes an invoice
    '''
    item = Invoice.objects.get(id=id)
    return render(request, 'invoice/info.html', {'invoice': item})


def list(request):
    ''' Get a list of all auction items for the current year's auction.
    '''
    items = Invoice.objects.filter(year=lambda: datetime.datetime.now().year)
    context = {'invoices': items,
               }
    return render(request, 'invoice/invoice_list.html', context)

def confirm_delete(request, id):
    return redirect('home')


def delete(request, id):
    item = Invoice.objects.get(id=id)
    item.delete()
    return redirect('invoice_list')

