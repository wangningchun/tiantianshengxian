# coding=utf-8
from django.shortcuts import render,redirect
from models import FreshInfo
from django.template import RequestContext
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from . import decorator
from hashlib import sha1
# Create your views here.
def register(request):
    return render(request,'fresheveryday/register.html')
def login(request):
    return render(request,'fresheveryday/login.html')
@decorator.login
def cart(request):
    return render(request,'fresheveryday/cart.html')

def place_order(request):
    return render(request,'fresheveryday/place_order.html')

def detail(request):
    return render(request,'fresheveryday/detail.html')

@decorator.login
def user_center_info(request):
    name = request.session['user_name']
    if name:
        data = FreshInfo.objects.get(fname=name)
        phone = data.fphone
        add = data.faddress
        return render(request,'fresheveryday/user_center_info.html',{'name':name,'phone':phone,'add':add})

    else:
        return render(request,'fresheveryday/index.html')
@decorator.login
def user_center_order(request):
    return render(request,'fresheveryday/user_center_order.html')

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