from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from list.forms import ItemForm
from list.models import *


def home_page(request):
    return render(request, 'list/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            new_item_text = request.POST['text']
            Item.objects.create(text=new_item_text, list=list_)
            return redirect(list_)

    return render(request, 'list/list.html', {'list': list_, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        new_item_text = request.POST.get('text', '')
        Item.objects.create(text=new_item_text, list=list_)
        return redirect(list_)
    else:
        return render(request, 'list/home.html', {'form': form})
