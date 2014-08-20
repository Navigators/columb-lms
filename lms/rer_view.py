# -*-coding:utf-8 -*-
from datetime import timedelta
import json
import re
import urllib2

from django.contrib.auth import authenticate
from django.core import serializers
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.utils.timezone import now

from lms.login_view import is_login_rer
from lms.models import Books, BookCate, LoanList, Readers, Comments


def reader_index(request):
    if not is_login_rer(request):
        return HttpResponseRedirect('/index/')
    
    if request.GET.get("json_new"):
        data = serializers.serialize('json', Books.objects.all(), ensure_ascii=False, use_natural_keys=True)
        return HttpResponse(data, content_type='json')
    
    if request.GET.get("json_cate"):
        data = serializers.serialize('json', Books.objects.filter(cate__id=request.GET.get("json_cate")), ensure_ascii=False, use_natural_keys=True)
        return HttpResponse(data, content_type='json')
    
    if request.GET.get("json_name"):
        data = serializers.serialize('json', Books.objects.filter(name=request.GET.get("json_name")), ensure_ascii=False, use_natural_keys=True)
        return HttpResponse(data, content_type='json')
    
    popular_books = Books.objects.all()[0:3]
    book_cates = BookCate.objects.all()
    return render(request, 'lms/reader/index.html', {'username':request.user.username,
                                                      'popular_books':popular_books,
                                                      'book_cates':book_cates,
                                                      }
                  )

def reader_loan(request):
    if not is_login_rer(request):
        return HttpResponseRedirect('/index/')
    error_query = ""
    query_list = LoanList.objects.all()
    
    if request.GET.get("json_id"):
        if request.GET.get("json_comment"):
            comment = Comments.objects.filter(loan__id=request.GET.get("json_id"))
            if comment:
                comment[0].content = request.GET.get("json_comment")
                comment[0].save()
            else:
                loan_record = LoanList.objects.get(id=request.GET.get("json_id"))
                Comments(loan=loan_record, content=request.GET.get("json_comment")).save()
            
        comment = Comments.objects.filter(loan__id=request.GET.get("json_id"))  
        data = serializers.serialize('json', comment, ensure_ascii=False)
        return HttpResponse(data, content_type='json')
    
    
    if request.GET.get("json_name")\
        or request.GET.get("json_date_from")\
        or request.GET.get("json_date_to")\
        or request.GET.get("json_status"):
        
        if request.GET.get("json_name"):
            query_list = query_list.filter(copy__book__name=request.GET.get("json_name"))
        if request.GET.get("json_date_from"):
            date_time_from = datetime.strptime(request.GET.get("json_date_from"), "%Y-%m-%d")
            query_list = query_list.filter(loan_date_time__gte=date_time_from)
        if request.GET.get("json_date_to"):
            date_time_to = datetime.strptime(request.GET.get("json_date_to"), "%Y-%m-%d")
            query_list = query_list.filter(loan_date_time__lte=date_time_to)
        if request.GET.get("json_status"):
            code_num = request.GET.get("json_status")
            if code_num == "1":
                query_list = query_list.filter(is_return=False, should_return_date__gte=now().date() + timedelta(days=0))
            elif code_num == "2":
                query_list = query_list.filter(is_return=True)
            elif code_num == "3":
                query_list = query_list.filter(is_return=False, should_return_date__lt=now().date() + timedelta(days=0))
            data = serializers.serialize('json', query_list, ensure_ascii=False, use_natural_keys=True)
            return HttpResponse(data, content_type='json')
    else:
        error_query = "请先选择查询条件后再进行查询"
    
    return render(request, 'lms/reader/myLoan.html', {'username':request.user.username, 'error_query':error_query, })

def reader_point(request):
    return render(request, 'lms/reader/myPoint.html')

def reader_profile(request):
    if not is_login_rer(request):
        return HttpResponseRedirect('/index/')
    
    reader = Readers.objects.get(username=request.user.username)
    if request.method == "POST":
        old_pd = request.POST['oldPassword']
        new_pd1 = request.POST['newPassword1']
        new_pd2 = request.POST['newPassword2']
        if old_pd and new_pd1 and new_pd2:
            user = authenticate(username=request.user.username, password=old_pd)
            if user is not None and user.is_active:  
                if new_pd1 == new_pd2:
                    user.set_password(new_pd1) 
                    user.save()
                    change_pd_error = ""
                    return HttpResponseRedirect('/index/')
                else:
                    change_pd_error = "Enter the new password twice inconsistent!"
                    return render(request, 'lms/reader/myProfile.html', {'username':request.user.username, 'reader':reader, 'change_pd_error':change_pd_error, })
            else:
                change_pd_error = "Enter the old password is incorrect!"
                return render(request, 'lms/reader/myProfile.html', {'username':request.user.username, 'reader':reader, 'change_pd_error':change_pd_error, })
        else:
            change_pd_error = "Please complete the form!"     
            return render(request, 'lms/reader/myProfile.html' , {'username':request.user.username, 'reader':reader, 'change_pd_error':change_pd_error, })  
    
    return render(request, 'lms/reader/myProfile.html' , {'username':request.user.username, 'reader':reader, })

def reader_review(request):
    if not is_login_rer(request):
        return HttpResponseRedirect('/index/')
    
    comments = Comments.objects.filter(loan__reader__username=request.user.username)
    return render(request, 'lms/reader/myReview.html', {'username':request.user.username, 'comments':comments, })

def reader_buy_book(request):
    if not is_login_rer(request):
        return HttpResponseRedirect('/index/')
    
    buy_book_msg=""
    if request.method == "POST":
        isbn = request.POST["isbn"]
        reason = request.POST["reason"]
        
        #缺少较完善的后台验证
        pattern = re.compile(u"^\d{10}$|^\d{13}$")
        if not pattern.search(isbn):
            buy_book_msg="申请购买图书的ISBN号格式不正确，请重新输入！。"
        elif 0:
            #查找是否申请购买的图书已有
            pass
        else:
            reader=Readers.objects.filter(username=request.user.username)[0]
        
#         data = urllib2.urlopen("http://10.167.129.109:3000/ISBNService/" + isbn).read()
#         book=json.loads(data)
#         reader.bookstoapply_set.create(
#                                      name=book["bookName"],
#                                      author=book["author"],
#                                      publisher=book["publisher"],
#                                      isbn=book["ISBN"],
#                                      price=book["price"],
#                                      reason=reason,
#                                      )
            reader.booksapply_set.create(
                                     name="娃哈哈",
                                     author="夏赟丞",
                                     publisher="天朝出版社",
                                     isbn="1231231231231",
                                     price="$29",
                                     reason="sss",
                                     )
            buy_book_msg="申请买书成功,请耐心等候邮件通知结果。"
    return render(request, 'lms/reader/buyBook.html', {'username':request.user.username,'buy_book_msg':buy_book_msg,})
