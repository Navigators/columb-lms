# -*-coding:utf-8 -*-

from django.contrib.auth import authenticate, login as user_login, logout as user_logout 
from django.http.response import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    if request.method == "POST":
        if login(request):
            # 判断是那种类型的用户，目前默认是图书管理员
            return HttpResponseRedirect('/lib/index/')
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

def is_login(request):
    return request.user.is_authenticated()

def get_errorlogin_session(request):
    if "error_login" in request.session:
        return request.session['error_login']
    else:
        return None
