# models.py of columb

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
    
class Publishers(models.Model):
    name = models.CharField(max_length=200)
    input_code = models.CharField(max_length=200) 
    isbn = models.CharField(max_length=40)
    place = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name    
    
class BookCate(models.Model):
    parent_id = models.IntegerField(default=0) 
    code = models.CharField(max_length=40) 
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
    
class ReaderCate(models.Model):
    name = models.CharField(max_length=80) 
    limit_books_count = models.IntegerField() 
    limit_days = models.IntegerField() 
    reloan_times = models.IntegerField() 
    reloan_days = models.IntegerField()
    loan_books_jp = models.BooleanField()
    
    def __unicode__(self):
        return self.name
    
class Librarians(User):
    code = models.CharField(max_length=40) 
    pwd = models.CharField(max_length=200) 
    title = models.CharField(max_length=40) 
    corp = models.ForeignKey(Items, related_name="librarian_corp") 
    dept = models.ForeignKey(Items, related_name="librarian_dept") 
    is_lock = models.BooleanField() 
    memo = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.username
    
    def save(self):
        self.password = make_password(self.pwd)
        self.pwd = self.password
        super(Librarians, self).save()
    
class Readers(User):
    input_code = models.CharField(max_length=40) 
    code = models.CharField(max_length=40)
    pwd = models.CharField(max_length=200)
    name = models.CharField(max_length=40)
    card_id = models.CharField(max_length=40) 
    cate = models.ForeignKey(ReaderCate) 
    sex = models.BooleanField() 
    birth_date = models.DateField() 
    corp = models.ForeignKey(Items, related_name="readers_corp") 
    dept = models.ForeignKey(Items, related_name="readers_dept") 
    id_card = models.CharField(max_length=36)
    work_card = models.CharField(max_length=36) 
    work_phone = models.CharField(max_length=40) 
    home_phone = models.CharField(max_length=40) 
    mobile_phone = models.CharField(max_length=40)  
    address = models.CharField(max_length=100)
    memo = models.CharField(max_length=100)
    operator = models.ForeignKey(Librarians)
    pic_location = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.username
    
    def save(self):
        self.password = make_password(self.pwd)
        self.pwd = self.password
        super(Readers, self).save()
        
class Books(models.Model):
    isbn = models.CharField(max_length=40) 
    name = models.CharField(max_length=200) 
    input_code = models.CharField(max_length=200) 
    author = models.CharField(max_length=200) 
    type = models.CharField(max_length=80) 
    cate = models.ForeignKey(BookCate) 
    publisher = models.ForeignKey(Publishers)
    publish_date = models.DateField()
    price = models.FloatField() 
    keywords = models.CharField(max_length=400) 
    series_name = models.CharField(max_length=200) 
    edition_time = models.CharField(max_length=80) 
    language = models.CharField(max_length=80) 
    face_info = models.CharField(max_length=80) 
    addons = models.CharField(max_length=80) 
    cn = models.CharField(max_length=40) 
    publish_periods = models.CharField(max_length=80) 
    up_dept = models.CharField(max_length=400)
    content_intro = models.TextField() 
    memo = models.CharField(max_length=200) 
    total_count = models.IntegerField(default=0) 
    loan_count = models.IntegerField(default=0) 
    reg_date = models.DateField(auto_now_add=True) 
    operator = models.ForeignKey(Librarians)
    pic_location = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
    
class Bylaw(models.Model):
    sort_code = models.IntegerField() 
    title = models.CharField(max_length=100) 
    content = models.TextField() 
    memo = models.CharField(max_length=100) 
    reg_date = models.DateField(auto_now_add=True) 
    operator = models.ForeignKey(Librarians)
    
class Copies(models.Model):
    book = models.ForeignKey(Books) 
    barcode = models.CharField(max_length=80)
    code = models.CharField(max_length=80)
    state = models.ForeignKey(Items, related_name="copies_state")  
    room = models.ForeignKey(Items, related_name="copies_room") 
    position = models.ForeignKey(Items, related_name="copies_position") 
    volume_info = models.CharField(max_length=80) 
    price = models.FloatField() 
    reg_date = models.DateField(auto_now_add=True) 
    operator = models.ForeignKey(Librarians)
    
    def __unicode__(self):
        return self.code
    
class LoanList(models.Model):
    copy = models.ForeignKey(Copies) 
    book = models.ForeignKey(Books) 
    reader = models.ForeignKey(Readers) 
    loan_date_time = models.DateTimeField(auto_now_add=True) 
    should_return_date = models.DateField() 
    reloan_times = models.IntegerField() 
    reLoan_date = models.DateField() 
    is_return = models.BooleanField() 
    fact_return_date_time = models.DateTimeField() 
    loan_operator = models.ForeignKey(Librarians, related_name="loanlist_loan")
    return_operator = models.ForeignKey(Librarians, related_name="loanlist_return")
    praise = models.BooleanField()
    rating_score = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.id
    
class Comments(models.Model):
    loan = models.ForeignKey(LoanList)
    content = models.CharField(max_length=200) 
    create_date_time=models.DateTimeField(auto_now_add=True)   

class Par(models.Model):
    system_name = models.CharField(max_length=100) 
    corp_name = models.CharField(max_length=100) 
    is_exit_confirm = models.BooleanField() 
    is_show_user_list_on_login = models.BooleanField()  
    is_max_book_manager = models.BooleanField() 
    
    def __unicode__(self):
        return self.system_name   
    
class UserFun(models.Model):
    key = models.IntegerField() 
    name = models.CharField(max_length=32) 
    cate = models.IntegerField() 
    img_index = models.IntegerField() 
    memo = models.CharField(max_length=90) 
    code = models.IntegerField() 
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
    computer_name = models.CharField(max_length=40) 
    operator = models.ForeignKey(Librarians)
    memo = models.CharField(max_length=100)
    

    
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
