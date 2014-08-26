# -*-coding:utf-8 -*-

from django.contrib.auth import authenticate, login as user_login, logout as user_logout 
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from lms.models import Librarians, Readers


def index(request):
    if request.method == "POST":
        if login(request):
            # 判断是那种类型的用户
            if Librarians.objects.filter(username=request.user.username):
                return HttpResponseRedirect('/lib/index/')
            elif Readers.objects.filter(username=request.user.username):
                return HttpResponseRedirect('/rer/index/')
            else:
                # 超级管理员不许登录管理员端和读者端
                user_logout(request)
                return HttpResponseRedirect('/index/')
        else:
            return HttpResponseRedirect('/index/')
    else:
        user_logout(request)
        error_login = get_errorlogin_session(request)
        return render(request, 'lms/login.html', {'error_login':error_login})

def login(request):
    # fangz前台伪造post请求
    if request.user.is_authenticated():  
        user_logout(request)
        return False     
    if 'error_login' in request.session:
        del request.session['error_login']
    username = request.POST['username']  
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:  
        if user.is_active:
            user_login(request, user)
        else:  
            request.session['error_login'] = "This account is being used!"
            return False
    else:  
        request.session['error_login'] = "The username or password is wrong!"
        return False
    return True

def is_login_lib(request):
    if request.user.is_authenticated():
        if Librarians.objects.filter(username=request.user.username):
            return True
        else: 
            return False
    else:
        return False
    
def is_login_rer(request):
    if request.user.is_authenticated():
        if Readers.objects.filter(username=request.user.username):
            return True
        else: 
            return False
    else:
        return False

def get_errorlogin_session(request):
    if "error_login" in request.session:
        return request.session['error_login']
    else:
        return None

def get_lib_name(request):
    return Librarians.objects.get(username=request.user.username).name

def get_rer_name(request):
    return Readers.objects.get(username=request.user.username).name