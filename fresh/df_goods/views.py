from django.shortcuts import render
from models import *
from py_cart.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    # fruit = GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[0:3]
    # fruits = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[0:4]
    #
    # seafood = GoodsInfo.objects.filter(gtype_id=2).order_by('-gclick')[0:2]
    # seafoods = GoodsInfo.objects.filter(gtype_id=2).order_by('-id')[0:4]
    #
    # pulp = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[0:3]
    # pulps = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[0:4]
    #
    # #return HttpResponse(red)
    # context={
    #     'fruit': fruit,
    #     'fruits': fruits,
    #     'seafood':seafood,
    #     'seafoods':seafoods,
    #     'pulp':pulp,
    #     'pulps':pulps
    #
    # }
    # return render(request,'fresheveryday/index.html',context)

    typelist = TypeInfo.objects.all()
    if request.session.has_key('user_id'):
        cart = len(CartInfo.objects.all())
    else:
        cart=0
    list = []
    for types in typelist:
        list.append({
            'types':types,
            'fruit':types.goodsinfo_set.order_by('-gclick')[0:3],
            'fruits':types.goodsinfo_set.order_by('id')[0:4]
        })
    return render(request, 'fresheveryday/index.html', {'list':list,'len':cart})

def list(request,id,pid):
    list_type = TypeInfo.objects.get(id = int(id))
    list_type1 = list_type.goodsinfo_set.order_by('-id')[0:2]
    lists = GoodsInfo.objects.filter(gtype_id=int(id))
    if request.session.has_key('user_id'):
        cart = len(CartInfo.objects.all())
    else:
        cart=0
    re = request.GET
    if re.get('a') =='0':
        liset_gprice = lists.order_by('gprice')

    elif re.get('a') =='1':
        liset_gprice = lists.order_by('gclick')

    else:
        liset_gprice = lists.order_by('id')

    p = Paginator(liset_gprice, 5)
    pid = int(pid)
    if pid <=0:
        pid = 1
    elif pid > p.num_pages:
        pid = p.num_pages
    list2 = p.page(pid)
    plist = p.page_range
    return render(request, 'fresheveryday/list.html',
                  {'list2': list2, 'plist': plist, 'id': id, 'list_type1': list_type1,'len':cart})


def detail(request):
    if request.session.has_key('user_id'):
        cart = len(CartInfo.objects.all())
    else:
        cart=0
    re = request.GET
    pid = re.get('a')
    minute = GoodsInfo.objects.get(id=pid)
    minute.gclick = minute.gclick +1
    minute.save()
    newest = minute.gtype.goodsinfo_set.order_by('id')[0:2]
    response = render(request, 'fresheveryday/detail.html',{'minute':minute,'newest':newest,'len':cart})

    liulan = request.COOKIES.get('list','')
    if liulan == '':
        response.set_cookie('list',pid)
    else:
        liulan_list = liulan.split(',')
        if pid in liulan_list:
            liulan_list.remove(pid)
        liulan_list.insert(0,pid)
        if len(liulan_list)>5:
            liulan_list.pop()
        liulan2 = ','.join(liulan_list)
        response.set_cookie('list', liulan2)
    return response




