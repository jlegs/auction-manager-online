from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from manager.models.invoice import Invoice
from manager.models.attendee import Attendee
from manager.models.auction_item import AuctionItem
from manager.forms import AuctionItemForm, ItemSearchForm, YearForm
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def create(request):
    ''' creates a new auction item for the current year's auction.
    '''
    if request.POST:
        form = AuctionItemForm(request.POST)
        if form.is_valid():
            exists = AuctionItem.objects.filter(item_number=form.cleaned_data['item_number'], year=lambda: datetime.datetime.now().year)
            if not exists:
                item = form.save()
                messages.add_message(request, messages.SUCCESS, 'Auction Item created')
                return redirect('item_list')
            else:
                messages.add_message(request, messages.WARNING, 'Item with that number exists.')
                return redirect('item_list')
        else:
            context = {'form': form}
            return render(request, 'auction_item/add.html', context)
    else:
        form = AuctionItemForm()
        context = {'form': form,
                   }
        return render(request, 'auction_item/add.html', context)

@login_required
def update(request, id):
    ''' Updates an auction item record
    '''
    item = get_object_or_404(AuctionItem, id=id)

    if request.POST:
        form = AuctionItemForm(request.POST, instance=item)
        if form.is_valid():
            item = AuctionItem.objects.get(id=id)
            if form.cleaned_data['item_number'] != item.item_number:
                try:
                    exists = AuctionItem.objects.get(item_number=form.cleaned_data['item_number'], year=lambda: datetime.datetime.now().year)
                except ObjectDoesNotExist:
                    exists = None
                if exists:
                    messages.add_message(request, messages.WARNING, 'Another item already has the number %i.' % form.cleaned_data['item_number'])
                else:
                    item.item_number = form.cleaned_data['item_number']
                    item.save()
                    messages.add_message(request, messages.SUCCESS, 'Item Number successfully updated.')
            elif form.cleaned_data['winning_bid_number'] != item.winning_bid_number:
                try:
                    attendee = Attendee.objects.get(bid_number=form.cleaned_data['winning_bid_number'])
                except ObjectDoesNotExist:
                    messages.add_message(request, messages.WARNING, 'No attendee found with that bid number.')
                    return redirect('item_list')
                invoice, created = Invoice.objects.get_or_create(attendee=attendee)
                item.winning_bid_number = form.cleaned_data['winning_bid_number']
                invoice.items.add(item)
                messages.add_message(request, messages.SUCCESS, 'Winning bidder set for item %s.' % item.description)
                if form.cleaned_data['selling_price'] != item.selling_price:
                    item.selling_price = form.cleaned_data['selling_price']
                    messages.add_message(request, messages.SUCCESS, 'Selling price set.')
                item.save()
            else:
                form.save()
                messages.add_message(request, messages.WARNING, 'Item %s updated' % form.cleaned_data['description'])
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong in the validation of the form. Please try again and ensure all the information is correct')
        return redirect('item_list')
    else:
        form = AuctionItemForm(instance=item)
        context = {'auction_item': item,
                   'form': form,
                   }

    return render(request, 'auction_item/update.html', context)



@login_required
def info(request, id):
    ''' Get item's info
    '''
    item = AuctionItem.objects.get(id=id)
    return render(request, 'auction_item/info.html', {'item': item})


@login_required
def item_search(request):
    """
    Search for Item by item number
    """
    context = {}
    if request.POST:
        form = ItemSearchForm(request.POST)
        if form.is_valid():
            try:
                item = AuctionItem.objects.get(item_number=form.cleaned_data['item_number'])
                context['item'] = item
                context['form'] = form
            except Exception as e:
                context['error'] = e
        else:
            return render(request, 'quction_item/item_search.html', context)
    else:
        form = ItemSearchForm()
        context['form'] = form

    return render(request, 'auction_item/item_search.html', context)



@login_required
def unsold_item_list(request):
    ''' Get a list of all unsold auction items for the current year's auction.
    '''
    items = AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year, winning_bid_number__isnull=True)
    context = {'auction_items': items,
               }
    return render(request, 'auction_item/item_list.html', context)

@login_required
def past_items(request):
    ''' Get a list of all auction items for the a past year's auction.
    '''
    context = {}
    if request.POST:
        form = YearForm(request.POST)
        if form.is_valid():
            items = AuctionItem.objects.filter(year=form.cleaned_data['year'])
            context['auction_items'] = items
            context['year'] = form.cleaned_data['year']
        else:
            context['errors'] = form.errors
            context['form'] = form
        return render(request, 'auction_item/item_list.html', context)
    else:
        form = YearForm()
        context['form'] = form
    return render(request, 'auction_item/item_list.html', context)





@login_required
def list(request):
    ''' Get a list of all auction items for the current year's auction.
    '''
    items = AuctionItem.objects.filter(year=lambda: datetime.datetime.now().year)
    context = {'auction_items': items,
               }
    return render(request, 'auction_item/item_list.html', context)


@login_required
def delete(request, id):
    item = AuctionItem.objects.get(id=id)
    item.delete()
    return redirect('item_list')



