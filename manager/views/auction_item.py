from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login, logout as django_logout
from manager.models.invoice import Invoice
from manager.models.attendee import Attendee
from manager.models.auction_item import AuctionItem
from manager.forms import AuctionItemForm
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def create(request):
    ''' creates a new auction item for the current year's auction.
    '''
    if request.POST:
        form = AuctionItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            invoice = Invoice(total_amount=0)
            invoice.save()
            invoice.items.add(item)
            invoice.save()
            messages.add_message(request, messages.SUCCESS, 'Auction Item created')
            return redirect('item_list')
        else:
            context = {'form': form}
            return render(request, 'auction_item/add.html', context)
    else:
        form = AuctionItemForm()
        context = {'form': form,
                   }
        return render(request, 'auction_item/add.html', context)
    return redirect('item_list')


def update(request, id):
    ''' Updates an auction item record
    '''
    item = get_object_or_404(AuctionItem, id=id)

    if request.POST:
        form = AuctionItemForm(request.POST, instance=item)
        if form.is_valid():
            print form,
            print form.cleaned_data
            # Set a list of bid numbers so we can check if the winning bid number entered is valid
            bid_numbers = [attendee.bid_number for attendee in Attendee.objects.filter(year=datetime.datetime.now().year)]
            if form.cleaned_data['winning_bid_number'] in bid_numbers:
                if form.cleaned_data['selling_price']:
                    invoice = form.cleaned_data['invoice']
                    invoice.set_total()
                    invoice.save()
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Auction Item updated')
            else:
                messages.add_message(request, messages.WARNING, 'That Bid Number Does Not Exist')
            return redirect('item_list')
        else:
            return redirect('item_info', id)
    else:
        form = AuctionItemForm(instance=item)
        context = {'auction_item': item,
                   'form': form,
                   }

    return render(request, 'auction_item/update.html', context)



def info(request, id):
    ''' Unimplemented
    '''
    item = AuctionItem.objects.get(id=id)
    return render(request, 'auction_item/info.html', {'item': item})


def list(request):
    ''' Get a list of all auction items for the current year's auction.
    '''
    items = AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year)
    context = {'auction_items': items,
               }
    return render(request, 'auction_item/item_list.html', context)

def confirm_delete(request, id):
    return redirect('home')


def delete(request, id):
    item = AuctionItem.objects.get(id=id)
    item.delete()
    return redirect('item_list')

