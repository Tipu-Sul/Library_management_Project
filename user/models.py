from django.db import models
from django.contrib.auth.models import User
from. const import GENDER_TYPE

# Create your models here.
class UserAccount(models.Model):
    user=models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    account_no=models.IntegerField(unique=True)
    birth_date=models.DateTimeField(null=True, blank=True)
    gender=models.CharField(max_length=50,choices=GENDER_TYPE)
    initial_deposit_date=models.DateTimeField(auto_now_add=True)
    balance=models.DecimalField(max_digits=8,default=0,decimal_places=2)
    def __str__(self):
        return str(self.account_no) 
    
class UserAddress(models.Model):
    user=models.OneToOneField(User, related_name="address",on_delete=models.CASCADE)
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    postal_code=models.IntegerField()
    country=models.CharField(max_length=100)
    def __str__(self):
        return str(self.user.email)
    
class BorrowBook(models.Model):
    user=models.ForeignKey(User, related_name="book", on_delete=models.CASCADE)
    book_name=models.CharField(max_length=100)
    book_price=models.DecimalField(max_digits=4, decimal_places=2,null=True, blank=True)
    balance_A_B_Book=models.DecimalField(max_digits=4, decimal_places=2,null=True, blank=True)
    borrow_date=models.DateField(auto_now_add=True)
    

