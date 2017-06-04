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

def list(request,id,pid):
    list_type = TypeInfo.objects.get(id = int(id))
    list_type1 = list_type.goodsinfo_set.order_by('-id')[0:2]
    lists = GoodsInfo.objects.filter(gtype_id=int(id))
    re = request.GET
    if re.get('a') =='0':
        liset_gprice = lists.order_by('gprice')
        p = Paginator(liset_gprice, 2)
        list2 = p.page(pid)
        plist = p.page_range
        return render(request, 'fresheveryday/list.html', {'list2': list2, 'plist': plist, 'id': id,'list_type1':list_type1})
    elif re.get('a') =='1':
        liset_gprice = lists.order_by('gclick')
        p = Paginator(liset_gprice, 2)
        list2 = p.page(pid)
        plist = p.page_range
        return render(request, 'fresheveryday/list.html', {'list2': list2, 'plist': plist, 'id': id,'list_type1':list_type1})
    else:

        p = Paginator(lists, 2)
        list2 = p.page(pid)
        plist = p.page_range
        return render(request,'fresheveryday/list.html',{'list2':list2,'plist':plist,'id':id,'list_type1':list_type1})


def detail(request):
    re = request.GET
    pid = re.get('a')
    minute = GoodsInfo.objects.get(id=pid)
    return render(request, 'fresheveryday/detail.html',{'minute':minute})



