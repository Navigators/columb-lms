from django.db import models

class ReaderCate(models.Model):
    ReaderCateName = models.CharField(max_length = 80) 
    LimitBooksCount = models.IntegerField() 
    LimitDays = models.IntegerField() 
    ReLoanTimes = models.IntegerField() 
    ReLoanDays = models.IntegerField()
    #rights to loan japanese booksadd by guoyuan
    LoanJpBooks = models.BooleanField()
    
class Readers(models.Model):
    ReaderName = models.CharField(max_length = 40) 
    ReaderInputCode = models.CharField(max_length = 40) 
    ReaderCode = models.CharField(max_length = 40) 
    CardID = models.CharField(max_length = 40) 
    ReaderCate = models.ForeignKey(ReaderCate) 
    Sex = models.BooleanField() 
    BirthDate = models.DateField() 
    CorpName = models.ForeignKey(Items) 
    Dept = models.ForeignKey(Items) 
    IDCard = models.CharField(max_length = 36) 
    WorkPhone = models.CharField(max_length = 40) 
    HomePhone = models.CharField(max_length = 40) 
    MobilePhone = models.CharField(max_length = 40) 
    EMail = models.CharField(max_length = 80) 
    Address = models.CharField(max_length = 100) 
    RegDate = models.DateTimeField() 
    PicLocation = models.CharField(max_length = 200)
    Operator = models.ForeignKey(Librarian)
