from django.contrib import admin
from.models import UserAccount,UserAddress,BorrowBook

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserAddress)
admin.site.register(BorrowBook)
