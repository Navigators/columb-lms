# models.py of columb

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name
    
    def natural_key(self):
        return (self.name)
    
class Company(models.Model):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name
    
    def natural_key(self):
        return (self.name)    

class BookType(models.Model):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name
    
    def natural_key(self):
        return (self.name)
    
class BookCate(models.Model):
    code = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
    
    def natural_key(self):
        return (self.code)
    
class CopyState(models.Model):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name
    
    def natural_key(self):
        return (self.name)
    
class ReaderCate(models.Model):
    name = models.CharField(max_length=80) 
    limit_books_count = models.IntegerField() 
    limit_days = models.IntegerField() 
    reloan_times = models.IntegerField() 
    reloan_days = models.IntegerField()
    loan_books_jp = models.BooleanField()
    
    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name)
    
class Librarians(User):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40, blank=True) 
    corp = models.ForeignKey(Company) 
    dept = models.ForeignKey(Department) 
    is_lock = models.BooleanField() 
    memo = models.CharField(max_length=100, blank=True)
    
    def __unicode__(self):
        return self.username
    
    def save(self):
        self.password = make_password(self.password)
        super(Librarians, self).save()
          
    def natural_key(self):
        return (self.name, self.username,) + (self.corp.natural_key(),) + (self.dept.natural_key(),)
    natural_key.dependencies = ['lms.Company', 'lms.Department']

    
class Readers(User):
    name = models.CharField(max_length=40)
    cate = models.ForeignKey(ReaderCate) 
    sex = models.BooleanField() 
    birth_date = models.DateField(blank=True, null=True) 
    corp = models.ForeignKey(Company) 
    dept = models.ForeignKey(Department) 
    work_phone = models.CharField(max_length=40, blank=True) 
    home_phone = models.CharField(max_length=40, blank=True) 
    mobile_phone = models.CharField(max_length=40, blank=True)  
    memo = models.CharField(max_length=100, blank=True)
    operator = models.ForeignKey(Librarians)
    pic_location = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return self.username
    
    def save(self):
        self.password = make_password(self.password)
        super(Readers, self).save()
        
    def natural_key(self):
        return (self.username,self.name)+(self.cate.natural_key(),)+(User.natural_key(self),)
    natural_key.dependencies=['lms.ReaderCate',]
        
class Books(models.Model):
    isbn = models.CharField(max_length=40) 
    name = models.CharField(max_length=200) 
    input_code = models.CharField(max_length=200) 
    author = models.CharField(max_length=200) 
    book_type = models.ForeignKey(BookType) 
    cate = models.ForeignKey(BookCate)
    publisher = models.CharField(max_length=80)
    publish_date = models.DateField(auto_now_add=True)
    publish_addr = models.CharField(max_length=80)
    price = models.CharField(max_length=40) 
    keywords = models.CharField(max_length=400, blank=True) 
    series_name = models.CharField(max_length=200, blank=True) 
    edition_time = models.CharField(max_length=80, blank=True) 
    language = models.CharField(max_length=80, blank=True) 
    face_info = models.CharField(max_length=80, blank=True) 
    addons = models.CharField(max_length=80, blank=True) 
    cn = models.CharField(max_length=40, blank=True) 
    publish_periods = models.CharField(max_length=80, blank=True) 
    up_dept = models.CharField(max_length=400, blank=True)
    content_intro = models.TextField(blank=True) 
    memo = models.CharField(max_length=200, blank=True) 
    total_count = models.IntegerField(default=0) 
    loan_count = models.IntegerField(default=0) 
    reg_date = models.DateField(auto_now_add=True)
    operator = models.ForeignKey(Librarians)
    pic_location = models.CharField(max_length=200, blank=True)
    rating_sum=models.IntegerField(default=0)
    rating_count=models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
    def natural_key(self):
        return (self.isbn, self.name) + (self.book_type.natural_key(),) + (self.cate.natural_key(),) + (self.operator.natural_key(),)
    natural_key.dependencies = ['lms.BookType', 'lms.BookCate', 'lms.Librarians']

    
class Bylaw(models.Model):
    title = models.CharField(max_length=100) 
    content = models.TextField() 
    memo = models.CharField(max_length=100, blank=True) 
    reg_date = models.DateField(auto_now_add=True) 
    operator = models.ForeignKey(Librarians)

    
class Copies(models.Model):
    book = models.ForeignKey(Books)
    barcode = models.CharField(max_length=80)
    state = models.ForeignKey(CopyState)
    volume_info = models.CharField(max_length=80, blank=True) 
    reg_date_time = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(Librarians)
    
    def __unicode__(self):
        return self.barcode
    
    def natural_key(self):
        return (self.barcode,) + (self.book.natural_key(),) + (self.state.natural_key(),) + (self.operator.natural_key(),)
    natural_key.dependencies = ['lms.Books', 'lms.CopyState', 'lms.Librarians']
    
class LoanList(models.Model):
    copy = models.ForeignKey(Copies) 
    reader = models.ForeignKey(Readers)
    loan_date_time = models.DateTimeField(auto_now_add=True) 
    should_return_date = models.DateField() 
    reloan_times = models.IntegerField(default=0) 
    reloan_date = models.DateField(blank=True, null=True)
    is_return = models.BooleanField(default=False) 
    fact_return_date_time = models.DateTimeField(blank=True, null=True) 
    loan_operator = models.ForeignKey(Librarians, related_name="loanlist_loan")
    return_operator = models.ForeignKey(Librarians, related_name="loanlist_return", blank=True, null=True)
    rating_score = models.IntegerField(default=0)
    
    def __unicode__(self):
        return str(self.id)
    
    def natural_key(self):
        return (self.rating_score,) + (self.copy.natural_key(),) + (self.reader.natural_key(),) + (self.loan_operator.natural_key(),) + (self.return_operator.natural_key(),)
    natural_key.dependencies = ['lms.Copies', 'lms.Readers', 'lms.Librarians']
    
class Comments(models.Model):
    loan = models.OneToOneField(LoanList)
    content = models.CharField(max_length=200) 
    create_date_time = models.DateTimeField(auto_now_add=True)   

    
class UserFun(models.Model):
    code = models.IntegerField() 
    name = models.CharField(max_length=40) 
    memo = models.CharField(max_length=90, blank=True) 
    is_used = models.BooleanField()
    
    def __unicode__(self):
        return self.name

    
class UserAccredit(models.Model):
    user = models.ForeignKey(Librarians)
    fun = models.ForeignKey(UserFun) 
    is_open = models.BooleanField()
    is_operate = models.BooleanField()
    is_print = models.BooleanField()

    
class UserLog(models.Model):
    log_date_time = models.DateTimeField(auto_now_add=True) 
    fun = models.ForeignKey(UserFun) 
    operate_content = models.CharField(max_length=8)  
    operator = models.ForeignKey(Librarians)
    memo = models.CharField(max_length=100, blank=True)
    
    
class BooksApply(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200) 
    publisher = models.CharField(max_length=80)  
    isbn = models.CharField(max_length=40)
    price = models.CharField(max_length=40)
    date=models.DateField(auto_now_add=True)
    reason= models.CharField(max_length=300) 
    requester = models.CharField(max_length=40)
    
class BooksBuy(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200) 
    publisher = models.CharField(max_length=80)  
    isbn = models.CharField(max_length=40) 
    price = models.CharField(max_length=40,blank=True)
    date=models.DateField(auto_now_add=True)
    operator = models.ForeignKey(Librarians)
    requester = models.ForeignKey(Readers)
    
class BooksArchive(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200) 
    publisher = models.CharField(max_length=80)  
    isbn = models.CharField(max_length=40) 
    price = models.CharField(max_length=40) 
    state = models.CharField(max_length=20)
    date=models.DateField(auto_now_add=True)
    operator = models.ForeignKey(Librarians)
    requester = models.CharField(max_length=40)

class PermPoint(models.Model):
    reader=models.ForeignKey(Readers)
    value=models.IntegerField(default=0)
    
class ExchangePoint(models.Model):
    reader=models.ForeignKey(Readers)
    value=models.IntegerField(default=0)
    operator = models.ForeignKey(Librarians)
    
class MessageTemplate(models.Model):
    subject = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    edit_time=models.DateField(auto_now_add=True)
