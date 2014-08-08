# -*-coding:utf-8 -*-

from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from lms.login_view import is_login


def reader_index(request):
    return render(request, 'lms/lib/index.html')

def lib_index(request):
    if not is_login(request):
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'lms/lib/index.html', {'username':request.user.username})
 
def lib_putaway(request):
    return render(request, 'lms/lib/addBook.html')

def lib_buybook(request):
    return render(request, 'lms/lib/buyBook.html')

def lib_retrieve(request):
    return render(request, 'lms/lib/addBook-new.html')

def lib_get_book_list(request):
    return render(request, 'lms/lib/booksInfo.html')

def lib_get_book_info(request):
    return render(request, 'lms/lib/addBook-new.html')

def lib_add_copies(request):
    return render(request, 'lms/lib/addBook-copy.html')


def lib_addbook_new(request):
#     if request.method == 'POST':
#         if request.POST['funno'] == '01':
#             return book_enter_base(request)
#     else:
        return render(request, 'lms/addbook_new.html') 
# def book_enter_base(request):
#     try:
#         #u = request.user
#         isbn = request.POST[''] 
#         name = request.POST['']
#         input_code = request.POST['']+''
#         author = request.POST['']
#         type = request.POST['']
#         publisher = Publisher.objects.get(name = request.POST[''])
#         publish_date = request.POST['']
#         price = request.POST['']
#         keywords = request.POST['']+''
#         series_name = request.POST['']+''
#         edition_time = request.POST['']+''
#         language = request.POST['']+''
#         face_info = request.POST['']+''
#         addons = request.POST['']+''
#         cn = request.POST['']+''
#         publish_periods = request.POST['']+''
#         up_dept = request.POST['']+''
#         content_intro = request.POST['']+''
#         memo = request.POST['']+''
#         total_count = 0
#         loan_count = 0
#         operater = 
#         piclocation = request.POST['']+''
