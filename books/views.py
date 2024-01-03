from django.shortcuts import render
from django.views.generic import DetailView
from. models import Book


# Create your views here.
class BookDetailsView(DetailView):
    model = Book
    # pk_url_kwargs = 'id'
    template_name='books/book_details.html'