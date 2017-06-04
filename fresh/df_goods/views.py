from django.shortcuts import render
from models import *
from django.http import HttpResponse
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    fruit = GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[0:3]
    fruits = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[0:4]

    seafood = GoodsInfo.objects.filter(gtype_id=2).order_by('-gclick')[0:2]
    seafoods = GoodsInfo.objects.filter(gtype_id=2).order_by('-id')[0:4]

    pulp = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[0:3]
    pulps = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[0:4]
    #return HttpResponse(red)
    context={
        'fruit': fruit,
        'fruits': fruits,
        'seafood':seafood,
        'seafoods':seafoods,
        'pulp':pulp,
        'pulps':pulps

    }
    return render(request,'fresheveryday/index.html',context)

def list(request,id):
    lists = GoodsInfo.objects.filter(gtype_id=id)
    p = Paginator(lists, 10)
    list2 = p.page(1)
    plist = p.page_range
    return render(request,'fresheveryday/list.html',{'list2':list2,'plist':plist})

def detail(request):
    re = request.GET
    pid = re.get('a')
    minute = GoodsInfo.objects.get(id=pid)
    return render(request, 'fresheveryday/detail.html',{'minute':minute})



