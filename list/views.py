from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from list.models import *


# Create your views here.

def home_page(request):
    return render(request, 'list/home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list/list.html', {
        'list': list_
    })


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
        return render(request, 'list/home.html', {"error": error})
    return redirect('/lists/%d/' % (list_.id,))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    new_item_text = request.POST.get('item_text', '')
    Item.objects.create(text=new_item_text, list=list_)
    return redirect('/lists/%d/' % (list_.id,))
