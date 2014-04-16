from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login, logout as django_logout
from manager.models.auction_item import AuctionItem
from manager.models.invoice import Invoice
from manager.models.auction_item import AuctionItem
from manager.forms import AuctionItemForm
import datetime
from django.core.exceptions import ObjectDoesNotExist


def create(request):
    ''' creates a new auction item for the current year's auction.
    '''
    if request.POST:
        form = AuctionItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect('item_list')
    else:
        form = AuctionItemForm()
        context = {'form': form,
                   'bid_number': bid_number,
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
            form.save()
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
    form = AuctionItemForm(request.POST)
    print form
    if form.is_valid():
        form.save()
        return redirect('item_info', id)
    else:
        return redirect('item_info', id)


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

