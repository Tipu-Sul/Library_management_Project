from django.shortcuts import render
from books.models import Book, Category

# Create your views here.

def home(request,category_slug=None):
    data=Book.objects.all()
    if category_slug is not None:
        category=Category.objects.get(slug=category_slug)
        data=Book.objects.filter(category=category)
    book_ctg=Category.objects.all()
    return render(request,'home.html',{'data':data, 'category':book_ctg})
