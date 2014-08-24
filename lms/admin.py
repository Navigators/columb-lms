from django.contrib import admin

from lms.models import BookCate, ReaderCate, Librarians, Readers, Books, \
    Bylaw, Copies, LoanList, Comments, UserFun, UserAccredit, UserLog, Company, \
    Department, BookType, CopyState, BooksApply, BooksBuy, BooksArchive, \
    PermCate, PermList, ExchangeCate, ExchangeList, MessageTemplate


# Register your models here.
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(BookType)
admin.site.register(CopyState)
admin.site.register(BookCate)
admin.site.register(ReaderCate)
admin.site.register(Librarians)
admin.site.register(Readers)
admin.site.register(Books)
admin.site.register(Bylaw)
admin.site.register(Copies)
admin.site.register(LoanList)
admin.site.register(Comments)
admin.site.register(UserFun)
admin.site.register(UserAccredit)
admin.site.register(UserLog)
admin.site.register(BooksApply)
admin.site.register(BooksBuy)
admin.site.register(BooksArchive)
admin.site.register(PermCate)
admin.site.register(PermList)
admin.site.register(ExchangeCate)
admin.site.register(ExchangeList)

admin.site.register(MessageTemplate)
