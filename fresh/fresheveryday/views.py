# coding=utf-8
from django.shortcuts import render,redirect
from models import FreshInfo
from django.template import RequestContext
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from . import decorator
from hashlib import sha1
from py_cart.models import *
from df_order.models import *
from django.core.paginator import Paginator,Page
# Create your views here.
def register(request):
    return render(request,'fresheveryday/register.html')
def login(request):
    return render(request,'fresheveryday/login.html')

def place_order(request):
    return render(request,'fresheveryday/place_order.html')

def detail(request):
    response = render(request, 'fresheveryday/detail.html')
    re = request.GET
    gid = re.get('a')
    liulan = request.COOKIES.get('list','')
    if liulan == '':
        response.set_cookie('list',gid)
    else:
        liulan_list = liulan.split(',')
        if liulan in liulan_list:
            liulan_list.remove(gid)
            liulan_list.insert(0,gid)
        if len(liulan_list)>5:
            liulan_list.pop()
        liulan2 = ','.join(liulan_list)
        response.set_cookie('list', liulan2)
    return response

@decorator.login
def user_center_info(request):
    cart = CartInfo.objects.all()
    name = request.session['user_name']
    data = FreshInfo.objects.get(fname=name)
    phone = data.fphone
    add = data.faddress
    goods_list = []
    liulan = request.COOKIES.get('list','')
    if liulan != '':
        liulan_list = liulan.split(',')
        for i in liulan_list:
            goods_list.append(GoodsInfo.objects.get(id = int(i)))
    return render(request,'fresheveryday/user_center_info.html',{'name':name,'phone':phone,'add':add,'len':len(cart),'goods_list':goods_list})

@decorator.login
def user_center_order(request):
    cart = CartInfo.objects.all()
    reder = OrderInfo.objects.filter(user_id=request.session['user_id'])
    return render(request,'fresheveryday/user_center_order.html',{'len':len(cart),'reder':reder})

def user_center_site(request):
    name = request.session['user_name']
    data = FreshInfo.objects.get(fname=name)
    address = data.faddress
    return render(request,'fresheveryday/user_center_site.html',{'address':address})

# 获取post表单内容,并提交到数据库
def pic_handle(request):
    re = request.POST
    fname = re.get('user_name')
    fpwd = re.get('pwd')
    femail = re.get('email')
    re = FreshInfo.objects.filter(fname = fname).count()
    if re ==1:
        return render(request, 'fresheveryday/register.html')
    else:
        s1 = sha1()
        s1.update(fpwd)
        fpwd = s1.hexdigest()
        data = FreshInfo.objects.create(fname=fname, fpwd=fpwd, femail=femail)
        data.save()
        return render(request, 'fresheveryday/login.html', {'name': fname})


def pic_handle1(request):
    re = request.POST
    name = re.get('username')
    pwd = re.get('pwd')
    s1 = sha1()
    s1.update(pwd)
    pwd = s1.hexdigest()
    jizhu = re.get('jizhu', 0)
    dict = FreshInfo.objects.filter(fname=name)
    if len(dict) == 1:
        if dict[0].fpwd == pwd:
            url = request.COOKIES.get('url','/')
            red = redirect(url)
            red.set_cookie('url','',max_age=-1)
            if jizhu !=0:
                red.set_cookie('name', name)
            else:
                red.set_cookie('uname', '', max_age=-1)

            request.session['user_id'] = dict[0].id
            request.session['user_name'] = name
            return red
        else:
            return render(request, 'fresheveryday/login.html',{'hint':1})
    else:
        return render(request,'fresheveryday/login.html',{'hint':0})

def pic_handle2(request):
    re = request.POST
    name = request.session['user_name']
    data = FreshInfo.objects.get(fname=name)
    data.frecipients =re.get('newname')
    data.faddress =re.get('app','')
    data.fyoubian =re.get('youbian')
    data.fphone =re.get('phone')
    data.save()
    address = data.faddress
    return render(request,'fresheveryday/user_center_site.html',{'address':address,'name':name})

def loginout(request):
    request.session.flush()
    return redirect('/')

def register1(request):
    uname = request.GET.get('uname')
    count = FreshInfo.objects.filter(fname = uname).count()
    return JsonResponse({'count':count})

def user_center_orders(request,id):
    rder = OrderInfo.objects.get(pk=id)
    rder.oIsPay = True
    rder.save()
    a='9988'
    return redirect('/urls/user_center_order/',{'a':a})