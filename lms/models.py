#models.py of columb
#created by guoyuan
#2014.8.4
from django.db import models
from django.contrib import admin


class BookCate(models.Model):
    BookCateParentID = models.IntegerField(default = 0) 
    BookCateCode = models.CharField(max_length = 40) 
    BookCateName = models.CharField(max_length = 200)

class Books(models.Model):
    ISBNISSN = models.CharField(max_length = 40) 
    BookName = models.CharField(max_length = 200) 
    BookInputCode = models.CharField(max_length = 200) 
    Author = models.CharField(max_length = 200) 
    BookType = models.CharField(max_length = 80) 
    BookCate = models.ForeignKey(BookCate) 
    Publisher = models.ForeignKey(Publisher) 
    BookPrice = models.FloatField(null = true) 
    Keywords = models.CharField(max_length = 400) 
    SeriesName = models.CharField(max_length = 200) 
    EditionTime = models.CharField(max_length = 80) 
    BookLanguage = models.CharField(max_length = 80) 
    BookFaceInfo = models.CharField(max_length = 80) 
    BookAddons = models.CharField(max_length = 80) 
    CN = models.CharField(max_length = 40) 
    PublishPeriods = models.CharField(max_length = 80) 
    UpDept = models.CharField(max_length = 400)
    ContentIntro = models.TextField() 
    Memo = models.CharField(max_length = 200) 
    TotalCount = models.IntegerField(default = 0) 
    LoanCount = models.IntegerField(default = 0) 
    RegDateTime = models.DateTimeField() 
    PicLocation = models.CharField(max_length = 200)
    Operator = models.ForeignKey(Librarian)

class BooksToBuy(models.Model):
    BookKind = models.CharField(max_length = 80)
    BookName = models.CharField(max_length = 200) 
    IsImport = models.BooleanField()
    Author = models.CharField(max_length = 200) 
    Publisher = models.ForeignKey(Publisher) 
    ISBNISSN = models.CharField(max_length = 40) 
    BookPrice = models.FloatField(null = true) 
    State = models.CharField(max_length = 20)
    Requester = models.CharField(max_length = 40)

    
class Bylaw(models.Model):
    SortCode = models.IntegerField() 
    BylawTitle = models.CharField(max_length = 100) 
    BylawContent = models.TextField() 
    Memo = models.CharField(max_length = 100) 
    RegDate = models.DateTimeField() 
    Operator = models.ForeignKey(Librarian)
    
class Copies(models.Model):
    BookID = models.IntegerField() 
    BookBarCode = models.CharField(max_length = 80) 
    BookState = models.ForeignKey(Items) 
    BookCode = models.CharField(max_length = 80) 
    BookRoom = models.ForeignKey(Items) 
    BookPos = models.ForeignKey(Items) 
    VolumeInfo = models.CharField(max_length = 80) 
    Price = models.FloatField(null = true) 
    RegDate = models.DateTimeField() 
    Operator = models.ForeignKey(Librarian)
    
class Items(models.Model):
    ItemCode = models.IntegerField(null = true) 
    ItemName = models.CharField(max_length = 80) 
    ItemCate = models.IntegerField()
    
class LoanList(models.Model):
    CopyID = models.ForeignKey(Copies) 
    BookID = models.ForeignKey(Books) 
    ReaderID = models.ForeignKey(Readers) 
    LoanDateTime = models.DateTimeField() 
    ShouldReturnDate = models.DateTimeField() 
    ReLoanTimes = models.IntegerField() 
    ReLoanDateTime = models.DateTimeField() 
    IsReturn = models.BooleanField() 
    FactReturnDateTime = models.DateTimeField() 
    LoanOperator = models.ForeignKey(Librarian)
    ReturnOperator = models.ForeignKey(Librarian)
   #review tag 8.5 16:30 
class Par(models.Model):
    SystemName = models.CharField(max_length = 100) 
    CorpName = models.CharField(max_length = 100) 
    IsExitConfirm = models.CharField(max_length = 40) 
    IsShowUserListOnLogin = models.CharField(max_length = 40) 
    IsMaxBookManager = models.CharField(max_length = 40)
    
class Publishers(models.Model):
    PublisherName = models.CharField(max_length = 200) 
    PublisherInputCode = models.CharField(max_length = 200) 
    PublisherISBN = models.CharField(max_length = 40) 
    PublisherPlace = models.CharField(max_length = 100)
    

    
class UserAccredit(models.Model):
    UserID = models.IntegerField() 
    Fun = models.ForeignKey(UserFun) 
    IsOpen = models.BooleanField()
    IsOperate = models.BooleanField()
    IsPr = models.BooleanField()
    
class UserFun(models.Model):
    FunKey = models.IntegerField() 
    FunName = models.CharField(max_length = 32) 
    FunCate = models.IntegerField() 
    ImgIndex = models.IntegerField() 
    FunMemo = models.CharField(max_length = 90) 
    FunCode = models.IntegerField(null = true) 
    IsUsed = models.CharField(max_length = 40)
    
class Librarian(models.Model):
    Code = models.CharField(max_length = 40) 
    Pwd = models.CharField(max_length = 40) 
    Name = models.CharField(max_length = 20) 
    Title = models.CharField(max_length = 40) 
    CorpName = models.ForeignKey(Items) 
    Dept = models.ForeignKey(Dept) 
    IsLock = models.CharField(max_length = 40) 
    Memo = models.CharField(max_length = 100)
    
class UserLog(models.Model):
    LogDateTime = models.DateTimeField() 
    Fun = models.ForeignKey(UserFun) 
    OperateContent = models.CharField(max_length = 8) 
    ComputerName = models.CharField(max_length = 40) 
    Operator = models.ForeignKey(Librarian)
    Memo = models.CharField(max_length = 100)
