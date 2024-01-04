from django.shortcuts import render
from django.views.generic import DetailView
from. models import Book
from user.models import Review


# Create your views here.
class BookDetailsView(DetailView):
    model = Book
    # pk_url_kwargs = 'id'
    template_name='books/book_details.html'
     
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['data']=Review.objects.filter(book=self.object)
        return context
