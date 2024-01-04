from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from. const import GENDER_TYPE,STAR

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
    user=models.ForeignKey(User, related_name="user_1", on_delete=models.CASCADE)
    book_id=models.IntegerField(null=True, blank=True)
    book_name=models.CharField(max_length=100)
    book_price=models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    balance_A_B_Book=models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    borrow_date=models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False, blank=True,null=True)
    def __str__(self):
        return self.book_name

class Review(models.Model):
    book=models.ForeignKey(Book, related_name="comment", on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    body=models.TextField(null=True, blank=True)
    star=models.CharField(max_length=50,choices=STAR,null=True,blank=True)
    time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by{self.name}'

