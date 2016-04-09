from django.shortcuts import render, redirect
from django.http import HttpResponse
from list.models import *


# Create your views here.

def home_page(request):
    return render(request, 'list/home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list/list.html', {
        'items': items
    })


def new_list(request):
    list_ = List.objects.create()
    new_item_text = request.POST.get('item_text', '')
    Item.objects.create(text=new_item_text, list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
