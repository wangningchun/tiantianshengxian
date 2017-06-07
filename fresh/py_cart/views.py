from django.shortcuts import render
from models import CartInfo
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

def cartadd(request,id):
    carts_num = CartInfo.objects.filter(goods=id).filter(user_id = request.session['user_id'])
    carts = carts_num[0]
    carts.count = carts.count+1
    carts.save()
    counts = CartInfo.objects.filter(goods=id)[0].count
    return JsonResponse({'counts':counts})

def cartminus(request,id):
    carts_num = CartInfo.objects.filter(goods=id).filter(user_id = request.session['user_id'])
    carts = carts_num[0]
    carts.count = carts.count-1
    carts.save()
    counts = CartInfo.objects.filter(goods=id)[0].count
    return JsonResponse({'counts':counts})

def delete(request,id):
    carts = CartInfo.objects.filter(goods=id)
    carts[0].delete()
    count = CartInfo.objects.all().count()
    return JsonResponse({'count':count})
