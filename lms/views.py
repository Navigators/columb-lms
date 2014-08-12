# -*-coding:utf-8 -*-
import datetime
import re
import time
import urllib
import urllib2

from django.core import serializers
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import simplejson, timezone
import django.utils
from django.views.decorators.csrf import csrf_exempt

from columb.settings import MEDIA_ROOT
from lms.login_view import is_login
from lms.models import Books, Librarians, BookCate, BookType, Copies, CopyState, \
    Readers, LoanList


def reader_index(request):
    return render(request, 'lms/lib/index.html')

def lib_index(request):
    if not is_login(request):
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'lms/lib/index.html', {'username':request.user.username})
 
def lib_putaway(request):
    if not is_login(request):
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'lms/lib/addBook.html', {'username':request.user.username})

def lib_buybook(request):
    return render(request, 'lms/lib/buyBook.html')

def lib_retrieve(request):
    # 验证用户登录
    if not is_login(request):
        return HttpResponseRedirect('/index/')
    
    # 返回json数据
    if request.GET.get('json_isbn'):
        data = urllib2.urlopen("http://10.167.129.109:3000/ISBNService/" + request.GET.get('json_isbn')).read()
        return HttpResponse(data, content_type='json')
    if request.GET.get('json_others'):
        others = urllib2.urlopen("http://api.douban.com/v2/book/isbn/" + request.GET.get('json_others') + "?fields=image,summary").read()
        return HttpResponse(others, content_type='json')
    
    # 正常加载
    isbn_string = request.POST['isbn']
    pattern = re.compile(u"^\d{10}$|^\d{13}$")
    if not pattern.search(isbn_string):
        return render(request, 'lms/lib/addBook.html', {'username':request.user.username})
    else:
        book = Books.objects.filter(isbn=isbn_string)
        if not book:
            return render(request, 'lms/lib/addBook-new.html', {
                                                                'username':request.user.username,
                                                                'isbn':isbn_string,
                                                                'types':BookType.objects.all(),
                                                                'date':time.strftime('%Y-%m-%d', time.localtime(time.time()))
                                                                }
                          )
        else:
            copy_list = Copies.objects.filter(book__isbn=isbn_string)
            return render(request, 'lms/lib/addBook-copy.html', {
                                                                 'username':request.user.username,
                                                                 'copy_list':copy_list,
                                                                 'isbn':isbn_string,
                                                                 }
                          )       

def lib_add_copies(request):
    # 验证用户登录
    if not is_login(request):
        return HttpResponseRedirect('/index/')
    
    # Ajax继续添加副本，并选择数量
    if request.GET.get('json_user') and request.GET.get('json_isbn'):
        lib = Librarians.objects.filter(username=request.GET.get('json_user'))[0]
        book = Books.objects.filter(isbn=request.GET.get('json_isbn'))[0]
        #
        if request.GET.get('json_add_num'):
            for i in range(int(request.GET.get('json_add_num'))):
                book.copies_set.create(
                                       barcode=get_barcode_format(book.isbn, book.copies_set.all().order_by('-reg_date_time')),
                                       state=CopyState.objects.get(name="可借"),
                                       operator=lib,
                                       )
                book.total_count += 1
                book.save()
        #
        if request.GET.get('json_code'):
            copy = Copies.objects.filter(barcode=request.GET.get('json_code'))[0]
            if request.GET.get('json_status'):
                copy.state = CopyState.objects.filter(name=request.GET.get('json_status'))[0]
                copy.operator = lib
                copy.save()
            else:
                copy.delete()
          
        data = serializers.serialize('json', Copies.objects.filter(book__isbn=request.GET.get('json_isbn')), ensure_ascii=False, use_natural_keys=True)
        return HttpResponse(data, content_type='json')
    
    # 入库及第一个副本
    isbn_string = request.POST['isbn']
    if not Books.objects.filter(isbn=isbn_string):
        lib = Librarians.objects.get(username=request.user.username)
#             pic_path=save_image("http://img3.douban.com/mpic/s1308874.jpg",isbn_string)
        lib.books_set.create(
                                isbn=isbn_string,
                                name=request.POST['bookName'],
                                input_code=request.POST['inputCode'],
                                author=request.POST['author'],
                                book_type=BookType.objects.get(name=request.POST['bookType']),
                                cate=BookCate.objects.get(code=request.POST['categoryID']),
                                publisher=request.POST['publisher'],
                                publish_date=get_publishdate_form(request.POST['publishDate']),
                                publish_addr=request.POST['publishAddr'],
                                price=request.POST['bookPrice'],
                                content_intro=request.POST['contentInfo'],
                                memo=request.POST['memo'],
#                                 pic_location =pic_path,
                            )
        book = Books.objects.get(isbn=isbn_string)
        book.copies_set.create(
                                barcode=get_barcode_format(book.isbn, book.copies_set.all().order_by('-reg_date_time')),
                                state=CopyState.objects.get(name="可借"),
                                operator=lib,
                                )
        book.total_count += 1
        book.save()
           
    # 无论是查看or保存并继续添加副本，都会有form表单
    isbn = Books.objects.get(isbn=request.POST['isbn']).isbn
    copy_list = Copies.objects.filter(book__isbn=request.POST['isbn'])
    return render(request, 'lms/lib/addBook-copy.html', {'username':request.user.username, 'copy_list':copy_list, 'isbn':isbn, })
    
def lib_get_book_list(request):
    if not is_login(request):
        return HttpResponseRedirect('/index/')
    
    # Ajaxs搜索图书
    if request.GET.get('json_user') and request.GET.get('json_isbn'):
        isbn_string = request.GET.get('json_isbn')
        pattern = re.compile(u"^\d{10}$|^\d{13}$")
        if pattern.search(isbn_string):
            data = serializers.serialize('json', Books.objects.filter(isbn=request.GET.get('json_isbn')), ensure_ascii=False, use_natural_keys=True)
            return HttpResponse(data, content_type='json')
    
    return render(request, 'lms/lib/booksInfo.html', {'username':request.user.username, 'book_list':Books.objects.all()})

def lib_get_book_info(request, isbn):
    book_info = Books.objects.get(isbn=int(isbn))
    return render(request, 'lms/lib/addBook-new.html', {'username':request.user.username, 'book':book_info})

def save_image(url, isbn):
    # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片  
    data = urllib.urlopen(url).read()  
    f = file(MEDIA_ROOT + "/" + isbn + ".jpg", "wb")
    f.write(data)  
    f.close()
    return str(MEDIA_ROOT + "/" + isbn + ".jpg")

def get_barcode_format(isbn, copies):
    if not copies:
        return isbn + "001"
    sub_str = copies[0].barcode
    last_id=int(sub_str[-3:])
    if str(last_id + 1).__len__() == 1:
        return isbn + "00" + str(last_id + 1)
    elif str(last_id + 1).__len__() == 2:
        return isbn + "0" + str(last_id + 1)
    elif str(last_id + 1).__len__() == 3:
        return isbn + str(last_id + 1)

def get_publishdate_form(date_string):
    if date_string.find(".") < 0:
        return django.utils.datetime_safe.datetime.strptime(date_string, "%Y")
    else:
        return django.utils.datetime_safe.datetime.strptime(date_string, "%Y.%m")
    
    
#################################借还模块##################################

@csrf_exempt
def lib_return_borrow(request):
    if not is_login(request):
        return HttpResponseRedirect('/index/')
    
    if request.method == 'POST':
        if request.POST['funno'] == '201':
            return lib_borrow_getcopy(request)
        if request.POST['funno'] == '202':
            return lib_borrow_getreader(request)
        if request.POST['funno'] == '203':
            return lib_borrow(request)
        if request.POST['funno'] == '204':
            return lib_return(request)
        if request.POST['funno'] == '205':
            return lib_reloan(request)
    else:
        return render(request, 'lms/lib/returnBorrow.html', {'username':request.user.username, })
def lib_borrow_getcopy(request):
    mbarcode = request.POST['text']
    r_dict = {}
    if Copies.objects.filter(barcode=mbarcode):
        mcopy = Copies.objects.get(barcode=mbarcode)
        r_dict['state'] = 'getcopy success'
        r_dict['copy'] = copy_to_dict(mcopy)
    else:
        r_dict['state'] = 'getcopy fail'
    r_json = simplejson.dumps(r_dict, ensure_ascii=False)
    return HttpResponse(r_json)
def copy_to_dict(copy):
    copydict = {}
    copydict['copyid'] = copy.id
    copydict['barcode'] = copy.barcode
    copydict['name'] = copy.book.name
    copydict['isbn'] = copy.book.isbn
    copydict['author'] = copy.book.author
    copydict['cate'] = copy.book.cate.name
    return copydict
    
def lib_borrow_getreader(request):
    card = request.POST['text']
    r_dict = {}
    if Readers.objects.filter(username=card):
        mreader = Readers.objects.get(username=card)
        r_dict['state'] = 'getreader success'
        r_dict['reader'] = reader_to_dict(mreader)
    else:
        r_dict['state'] = 'getreader fail'
    r_json = simplejson.dumps(r_dict, ensure_ascii=False)
    return HttpResponse(r_json)
def reader_to_dict(reader):
    readerdict = {}
    readerdict['readerid'] = reader.id
    readerdict['username'] = reader.username
    readerdict['name'] = reader.name
    readerdict['cate'] = reader.cate.name
    readerdict['corp'] = reader.corp.name
    readerdict['dept'] = reader.dept.name
    return readerdict

def loan_to_dict(loan):
    loandict = {}
    loandict['username'] = loan.reader.username
    loandict['readername'] = loan.reader.name
    loandict['dept'] = loan.reader.dept.name
    loandict['barcode'] = loan.copy.barcode
    loandict['bookname'] = loan.copy.book.name
    loandict['author'] = loan.copy.book.author
    loandict['loandatetime'] = loan.loan_date_time.strftime("%Y-%m-%d %H:%M:%S")
    loandict['reloantimes'] = loan.reloan_times
    if loan.reloan_date:
        loandict['reloandate'] = loan.reloan_date.strftime("%Y-%m-%d")
    else:
        loandict['reloandate'] = ""
    loandict['shouldreturndate'] = loan.should_return_date.strftime("%Y-%m-%d")
    loandict['operator'] = loan.loan_operator.name 
    return loandict

def lib_borrow(request):
    copyid = int(request.POST['copyid'])
    readerid = int(request.POST['readerid'])
    # check if reader exists
    if Readers.objects.filter(pk=readerid):
        mreader = Readers.objects.get(pk=readerid)
    else:
        return HttpResponse('{"state":"reader not found"}') 
    # check if copy exists
    if Copies.objects.filter(pk=copyid):
        mcopy = Copies.objects.get(pk=copyid)
    else:
        return HttpResponse('{"state":"copy not found"}') 
    # check if copy can be borrowed
    if LoanList.objects.filter(copy=mcopy, is_return=False):
        return HttpResponse('{"state":"copy is borrowed"}') 
    # check if reader can borrow japanese book
    if not mreader.cate.loan_books_jp:
        return HttpResponse('{"state":"cant borrow japanese books"}') 
    # check if reader has book that didnt return in time 
    loan_list_set = LoanList.objects.filter(reader=mreader, is_return=False)
    if loan_list_set:
        for ml in loan_list_set:
            if ml.should_return_date < timezone.now().date():
                return HttpResponse('{"state":"book beyond date"}') 
    # modify next line when user module added!
    mloan_operator = Librarians.objects.get(username=request.user.username)
    mis_return = False
    mpraise = False
    if LoanList.objects.filter(copy=mcopy, is_return=False):
        return HttpResponse('{"state":"loan record not found"}') 
    else:
        mlimit_days = mreader.cate.limit_days
        mshould_return_date = timezone.now() + datetime.timedelta(days=mlimit_days)
        LoanList.objects.create(copy=mcopy, reader=mreader, should_return_date=mshould_return_date, is_return=mis_return, loan_operator=mloan_operator, praise=mpraise)
        r_dict = {}
        r_dict['state'] = 'borrow success'
        r_dict['copy'] = copy_to_dict(mcopy) 
        r_dict['reader'] = reader_to_dict(mreader)
        loan_list_set = LoanList.objects.filter(reader=mreader, is_return=False)
        loan_list = []
        if loan_list_set:
            for ml in loan_list_set:
                loan_list.append(loan_to_dict(ml))
        r_dict['loanlist'] = loan_list
        r_json = simplejson.dumps(r_dict, ensure_ascii=False)
        return HttpResponse(r_json)

def lib_return(request):
    copyid = int(request.POST['copyid'])
    if Copies.objects.filter(pk=copyid):
        mcopy = Copies.objects.get(pk=copyid)
    else:
        return HttpResponse('{"state":"copy not found"}') 
    if LoanList.objects.filter(copy=mcopy, is_return=False):
        mloan = LoanList.objects.get(copy=mcopy, is_return=False)
    else:
        return HttpResponse('{"state":"loan record not found"}') 
    # modify next line when user module added!
    mreturn_operator = Librarians.objects.get(username=request.user.username)
    mreader = mloan.reader
    if mloan.is_return == False:
        mloan.is_return = True
        mloan.return_operator = mreturn_operator
        mloan.fact_return_date_time = timezone.now()
        mloan.save()
        r_dict = {}
        r_dict['state'] = 'return success'
        r_dict['copy'] = copy_to_dict(mcopy) 
        r_dict['reader'] = reader_to_dict(mreader)
        loan_list_set = LoanList.objects.filter(reader=mreader, is_return=False)
        loan_list = []
        if loan_list_set:
            for ml in loan_list_set:
                loan_list.append(loan_to_dict(ml))
        r_dict['loanlist'] = loan_list
        r_json = simplejson.dumps(r_dict, ensure_ascii=False)
        return HttpResponse(r_json)

def lib_reloan(request):
    copyid = int(request.POST['copyid'])
    # check if copy exists
    if Copies.objects.filter(pk=copyid):
        mcopy = Copies.objects.get(pk=copyid)
    else:
        return HttpResponse('{"state":"copy not found"}') 
    # check if loan record exists
    if LoanList.objects.filter(copy=mcopy, is_return=False):
        mloan = LoanList.objects.get(copy=mcopy, is_return=False)
    else:
        return HttpResponse('{"state":"loan record not found"}') 
    mreader = mloan.reader
    # check if reader has book that didnt return in time 
    loan_list_set = LoanList.objects.filter(reader=mreader, is_return=False)
    if loan_list_set:
        for ml in loan_list_set:
            if timezone.now().date() > ml.should_return_date:
                return HttpResponse('{"state":"book beyond date"}') 

    # check reloan times
    if mloan.reloan_times < mreader.cate.reloan_times:
        mloan.reloan_times += 1 
    else:
        return HttpResponse('{"state":"cannot reloan any more"}') 
    # check if on five days before deadline
    if timezone.now().date() < mloan.should_return_date - datetime.timedelta(days=5):
        return HttpResponse('{"state":"cannot reloan yet"}') 
    # modify next line when user module added!
    mloan.reloan_operator = Librarians.objects.get(username=request.user.username)
    mloan.should_return_date = mloan.should_return_date + datetime.timedelta(days=mreader.cate.reloan_days)
    mloan.save()
    r_dict = {}
    r_dict['state'] = 'reloan success'
    r_dict['copy'] = copy_to_dict(mcopy) 
    r_dict['reader'] = reader_to_dict(mreader)
    loan_list_set = LoanList.objects.filter(reader=mreader, is_return=False)
    loan_list = []
    if loan_list_set:
        for ml in loan_list_set:
            loan_list.append(loan_to_dict(ml))
    r_dict['loanlist'] = loan_list
    r_json = simplejson.dumps(r_dict, ensure_ascii=False)
    return HttpResponse(r_json)
