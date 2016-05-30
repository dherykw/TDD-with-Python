from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from list.forms import ItemForm
from list.models import *


def home_page(request):
    return render(request, 'list/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            new_item_text = request.POST.get('item_text', '')
            item = Item(text=new_item_text, list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have any empty list item"

    return render(request, 'list/list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    new_item_text = request.POST.get('item_text', '')
    item = Item(text=new_item_text, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have any empty list item"
        return render(request, 'list/home.html', {'error': error})
    return redirect(list_)
