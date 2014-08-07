# models.py of columb

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import default


class Items(models.Model):
    code = models.IntegerField() 
    name = models.CharField(max_length=80)
    cate = models.IntegerField()
    
    def __unicode__(self):
        return self.name

admin.site.register(Items)
    
class Publishers(models.Model):
    name = models.CharField(max_length=200)
    isbn = models.CharField(max_length=40)
    place = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name    
admin.site.register(Publishers)
    
class BookCate(models.Model):
    code = models.CharField(max_length=40) 
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
admin.site.register(BookCate)
    
class ReaderCate(models.Model):
    name = models.CharField(max_length=80) 
    limit_books_count = models.IntegerField() 
    limit_days = models.IntegerField() 
    reloan_times = models.IntegerField() 
    reloan_days = models.IntegerField()
    loan_books_jp = models.BooleanField()
    
    def __unicode__(self):
        return self.name
admin.site.register(ReaderCate)
    
class Librarians(User):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40,blank=True) 
    corp = models.ForeignKey(Items, related_name="librarian_corp") 
    dept = models.ForeignKey(Items, related_name="librarian_dept") 
    is_lock = models.BooleanField() 
    memo = models.CharField(max_length=100,blank=True)
    
    def __unicode__(self):
        return self.username
    
admin.site.register(Librarians)
    
class Readers(User):
    name = models.CharField(max_length=40)
    cate = models.ForeignKey(ReaderCate) 
    sex = models.BooleanField() 
    birth_date = models.DateField(blank=True) 
    corp = models.ForeignKey(Items, related_name="readers_corp") 
    dept = models.ForeignKey(Items, related_name="readers_dept") 
    work_phone = models.CharField(max_length=40,blank=True) 
    home_phone = models.CharField(max_length=40,blank=True) 
    mobile_phone = models.CharField(max_length=40,blank=True)  
    memo = models.CharField(max_length=100,blank=True)
    operator = models.ForeignKey(Librarians)
    pic_location = models.CharField(max_length=200,blank=True)
    
    def __unicode__(self):
        return self.username

admin.site.register(Readers)
        
class Books(models.Model):
    isbn = models.CharField(max_length=40) 
    name = models.CharField(max_length=200) 
    input_code = models.CharField(max_length=200) 
    author = models.CharField(max_length=200) 
    book_type = models.CharField(max_length=80) 
    cate = models.ForeignKey(BookCate) 
    publisher = models.ForeignKey(Publishers)
    publish_date = models.DateField()
    price = models.CharField(max_length=40) 
    keywords = models.CharField(max_length=400,blank=True) 
    series_name = models.CharField(max_length=200,blank=True) 
    edition_time = models.CharField(max_length=80,blank=True) 
    language = models.CharField(max_length=80,blank=True) 
    face_info = models.CharField(max_length=80,blank=True) 
    addons = models.CharField(max_length=80,blank=True) 
    cn = models.CharField(max_length=40,blank=True) 
    publish_periods = models.CharField(max_length=80,blank=True) 
    up_dept = models.CharField(max_length=400,blank=True)
    content_intro = models.TextField(blank=True) 
    memo = models.CharField(max_length=200,blank=True) 
    total_count = models.IntegerField(default=0) 
    loan_count = models.IntegerField(default=0) 
    reg_date = models.DateField(auto_now_add=True) 
    operator = models.ForeignKey(Librarians)
    pic_location = models.CharField(max_length=200,blank=True)
    
    def __unicode__(self):
        return self.name
admin.site.register(Books)
    
class Bylaw(models.Model):
    title = models.CharField(max_length=100) 
    content = models.TextField() 
    memo = models.CharField(max_length=100,blank=True) 
    reg_date = models.DateField(auto_now_add=True) 
    operator = models.ForeignKey(Librarians)
admin.site.register(Bylaw)
    
class Copies(models.Model):
    book = models.ForeignKey(Books) 
    barcode = models.CharField(max_length=80)
    state = models.ForeignKey(Items, related_name="copies_state")  
    volume_info = models.CharField(max_length=80,blank=True) 
    reg_date_time = models.DateTimeField(auto_now_add=True) 
    operator = models.ForeignKey(Librarians)
    
    def __unicode__(self):
        return self.code
admin.site.register(Copies)
    
class LoanList(models.Model):
    copy = models.ForeignKey(Copies) 
    book = models.ForeignKey(Books) 
    reader = models.ForeignKey(Readers) 
    loan_date_time = models.DateTimeField(auto_now_add=True) 
    should_return_date = models.DateField() 
    reloan_times = models.IntegerField(default=0) 
    reLoan_date = models.DateField(blank=True) 
    is_return = models.BooleanField() 
    fact_return_date_time = models.DateTimeField(blank=True) 
    loan_operator = models.ForeignKey(Librarians, related_name="loanlist_loan")
    return_operator = models.ForeignKey(Librarians, related_name="loanlist_return")
    praise = models.BooleanField()
    rating_score = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.id
admin.site.register(LoanList)
    
class Comments(models.Model):
    loan = models.ForeignKey(LoanList)
    content = models.CharField(max_length=200) 
    create_date_time=models.DateTimeField(auto_now_add=True)   
admin.site.register(Comments)
    
class UserFun(models.Model):
    code = models.IntegerField() 
    name = models.CharField(max_length=40) 
    memo = models.CharField(max_length=90,blank=True) 
    is_used = models.BooleanField()
    
    def __unicode__(self):
        return self.name
admin.site.register(UserFun)
    
class UserAccredit(models.Model):
    user = models.ForeignKey(Librarians)
    fun = models.ForeignKey(UserFun) 
    is_open = models.BooleanField()
    is_operate = models.BooleanField()
    is_print = models.BooleanField()
admin.site.register(UserAccredit)
    
class UserLog(models.Model):
    log_date_time = models.DateTimeField(auto_now_add=True) 
    fun = models.ForeignKey(UserFun) 
    operate_content = models.CharField(max_length=8)  
    operator = models.ForeignKey(Librarians)
    memo = models.CharField(max_length=100,blank=True)
admin.site.register(UserLog)
    

    
# class BooksToBuy(models.Model):
#     BookKind = models.CharField(max_length = 80)
#     BookName = models.CharField(max_length = 200) 
#     IsImport = models.BooleanField()
#     Author = models.CharField(max_length = 200) 
#     Publisher = models.ForeignKey(Publishers) 
#     ISBNISSN = models.CharField(max_length = 40) 
#     BookPrice = models.FloatField() 
#     State = models.CharField(max_length = 20)
#     Requester = models.CharField(max_length = 40)
