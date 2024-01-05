from typing import Any
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from. models import BorrowBook,Review
from books.models import Book
from django.contrib import messages
from django.views.generic import FormView,TemplateView
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView, LogoutView
from. forms import RegistrationsForm,UpdateUserform,DepositForm,BookReviewForm
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
class UserCreateView(FormView):
    template_name='user/signup.html'
    form_class=RegistrationsForm
    success_url=reverse_lazy('profile')
    def form_valid(self, form):
        user=form.save()
        messages.success(self.request, "User created successfully")
        login(self.request,user)       
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['type']='SignUp'
        return context

class UserLoginView(LoginView):
    template_name='user/signup.html'
    def get_success_url(self):
        messages.success(self.request,'Logged in successfully')
        return reverse_lazy('profile')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['type']='Login'
        return context
    
# class UserLogoutView(LoginRequiredMixin,LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#             messages.success(self.request,'Logged out successfully')
#         return reverse_lazy('login')
    
class UserLogoutView(LoginRequiredMixin, LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Logged out successfully')
        return reverse_lazy('login')

    
class UserAcountUpdateView(LoginRequiredMixin,View):
    template_name='user/signup.html'

    def get(self,request):
        form=UpdateUserform(instance=request.user)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=UpdateUserform(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request,'Account updeted successfully')
            return redirect('profile')
        return render(request,self.template_name,{'form':form})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] ='User Update' 
        return context
    


class ProfileView(LoginRequiredMixin,TemplateView):
    template_name='user/profile.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['data']=BorrowBook.objects.filter(user=self.request.user)
        return context


class DepositView(LoginRequiredMixin,View):
    template_name='user/deposite.html'
    form_class = DepositForm
    # success_url =reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            account=self.request.user.account
            account.balance += amount 
            account.save(
            update_fields=['balance']
            )
            messages.success(self.request,'Deposit successfull')
            return redirect('profile')
        return render(request,self.template_name,{'form':form})

@login_required     
def book_borrow(request,id):
    book=Book.objects.get(pk=id)
    user_balance = request.user.account.balance
    price=book.book_price
    num_1=Decimal(user_balance)
    num_2=Decimal(price)
    num_3=num_1-num_2

    if book.book_quantity<1:
        messages.warning(request,'No stocks available')
        return redirect('profile')
    else:
        if user_balance>=book.book_price:
            # af_balance=user_balance - book.book_price
        
            borrow=BorrowBook.objects.create(
                user=request.user,
                book_id=id,
                book_name=book.book_name,
                book_price=book.book_price,
                balance_A_B_Book=num_3,
            )
            
            book.book_quantity-=1
            request.user.account.balance=num_3
            request.user.account.save(
                update_fields=['balance']
            )
            book.save()
            borrow.save()
            messages.success(request,'borrowed book successfully')
            return redirect('profile')
        else:
            messages.warning(request,'Insufficient balance')
        return redirect('profile')

@login_required
def Return_Book(request, id):
    book = get_object_or_404(Book, pk=id)

    # Find the BorrowBook instance for this user and book
    try:
        book_returned = BorrowBook.objects.get(book_id=id, user=request.user, returned=False)
    except BorrowBook.DoesNotExist:
        # Handle the case where no matching record is found
        # Redirect to an error page or show a message
        return redirect('profile')

    # Proceed with returning the book
    account = request.user.account
    account.balance += book.book_price
    book.book_quantity += 1
    book_returned.returned = True

    book.save(update_fields=['book_quantity'])
    account.save(update_fields=['balance'])
    book_returned.save(update_fields=['returned'])
    messages.success(request,'returned book successfully')
    return redirect('profile')



@login_required
def Book_review(request,id):
    book=Book.objects.get(pk=id)
    if request.method == 'POST':
        form=BookReviewForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data['body']
            star=form.cleaned_data['star']
            review=Review.objects.create(
                book=book,
                name=request.user.first_name,
                body=text,
                star=star,
            )
            review.save()
            messages.success(request,'Review successfull')
            return redirect('profile')
    else:
        form=BookReviewForm()
    return render(request,'user/signup.html',{'form':form,'type':'Review'})


   