from django.shortcuts import render
from models import CartInfo
from fresheveryday.models import *
from fresheveryday.decorator import *
from django.http import HttpResponse,JsonResponse
# Create your views here.
@login
def add(request,pid,num):
    carts_num = CartInfo.objects.filter(goods=pid)
    if len(carts_num) == 0:
        carts = CartInfo()
        carts.goods_id = int(pid)
        carts.count = int(num)
        carts.user_id = request.session['user_id']
        carts.save()
    else:
        carts = carts_num[0]
        carts.count+=int(num)
        carts.save()
    if request.is_ajax():
        return JsonResponse({'count':CartInfo.objects.filter(user_id=request.session['user_id']).count()})
    else:
        return redirect('/cart/cart/')

@login
def cart(request):
    list = CartInfo.objects.filter(user_id=request.session['user_id'])
    if request.session.has_key('user_id'):
        cart = len(CartInfo.objects.all())
    else:
        cart=0
    return render(request, 'fresheveryday/cart.html',{'list':list,'len':cart})

def count_change(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    carts_num = CartInfo.objects.filter(id=id)
    carts = carts_num[0]
    carts.count = count
    carts.save()
    return JsonResponse({'count':cart.count})

def delete(request):
    id = request.GET.get('id')
    cart = CartInfo.objects.get(id=id)
    cart.delete()
    return JsonResponse({'result':'ok'})

def place_order(request):
    user_id = request.session['user_id']
    user = FreshInfo.objects.get(id = user_id)
    gid = request.GET.getlist('gid')
    cart = CartInfo.objects.filter(id__in = gid)
    return render(request,'fresheveryday/place_order.html',{'cart':cart,'user':user})