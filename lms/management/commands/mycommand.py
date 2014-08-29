from django.core.management.base import BaseCommand,CommandError           
import os
from lms.models import Books, Librarians, BookCate, BookType, Copies, CopyState, \
    Readers, LoanList, ReaderCate, PermCate, PermList
from django.utils import timezone
import datetime

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class Command(BaseCommand):
    def handle(self, *args, **options):         
        _now_date = (timezone.now()-datetime.timedelta(days = 1)).date()
        _five_days_later = (timezone.now() + datetime.timedelta(days = 5)).date()
        _start_date = datetime.date(2010,1,1)
        _end_date = (timezone.now()- datetime.timedelta(days = 1)).date()
        _overdue_loans = LoanList.objects.filter(is_return = False,should_return_date__range = (_start_date,_end_date))
        _overdue_today = LoanList.objects.filter(is_return = False,should_return_date = _now_date)
        _overdue_five_days = LoanList.objects.filter(is_return = False,should_return_date = _five_days_later) 
        for tl in _overdue_today:
            print send_email2(tl)
        for tl in _overdue_five_days:
            print send_email(tl)
        for tl in _overdue_loans:
            tdate = tl.should_return_date
            diff =  datetime.date.today() - datetime.date(tdate.year,tdate.month,tdate.day) 
            if (diff.days % 5) == 0:
                print send_email2(tl)
            _tperm_cate = PermCate.objects.get(id=3)
            _treader = tl.reader
            _treader.per_point += _tperm_cate.value
            _treader.save()
            PermList.objects.create(reader = _treader,cate=_tperm_cate,value = _tperm_cate.value)

        print 'time task complete'

def send_email(LoanList):
        return os.popen('java -jar /home/guoyfnst/dev/place/django/columb/columbmail.jar overdue '+LoanList.reader.name.decode('UTF-8')+' '+LoanList.copy.book.name.decode('UTF-8')+' '+LoanList.loan_date_time.strftime("%Y-%m-%d%H:%M:%S")+' '+LoanList.should_return_date.strftime("%Y-%m-%d")+' '+LoanList.reader.email)
def send_email2(LoanList):
        return os.popen('java -jar /home/guoyfnst/dev/place/django/columb/columbmail.jar overdue2 '+LoanList.reader.name.decode('UTF-8')+' '+LoanList.copy.book.name.decode('UTF-8')+' '+LoanList.loan_date_time.strftime("%Y-%m-%d%H:%M:%S")+' '+LoanList.should_return_date.strftime("%Y-%m-%d")+' '+LoanList.reader.email)
        
