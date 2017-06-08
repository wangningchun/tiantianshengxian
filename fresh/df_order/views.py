from django.shortcuts import render,redirect
from models import *
from fresheveryday.models import *
from py_cart.models import *
from df_goods.models import *
from datetime import datetime
from django.db import transaction
# Create your views here.
@transaction.atomic
def order(request):
    post = request.POST
    address = post.get('address')
    order_id = post.getlist('order_id')
    sid = transaction.savepoint()
    try:
        order = OrderInfo()
        now = datetime.now()
        user_id = request.session['user_id']
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id)
        order.odate = now
        order.oaddress = address
        order.user_id = user_id
        order.ototal =0
        order.save()
        counts = 0
        for item in order_id:
            cart = CartInfo.objects.get(pk=item)
            if cart.goods.gkucun >= cart.count:
                cart.goods.gkucun -= cart.count
                cart.goods.save()
                detail = OrderDetailInfo()
                detail.count = cart.count
                detail.price = cart.goods.gprice
                detail.order = order
                detail.goods = cart.goods
                detail.save()

                counts += cart.goods.gprice*cart.count
                cart.delete()
            else:
                transaction.savepoint_rollback(sid)
                return redirect('/cart/cart/')
        order.ototal = counts
        order.save()
        transaction.savepoint_commit(sid)
        return redirect('/urls/user_center_order/')
    except:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/cart/')