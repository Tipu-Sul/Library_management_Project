from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse_lazy
from. models import BorrowBook
from books.models import Book
from django.contrib import messages
from django.views.generic import FormView,TemplateView
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView, LogoutView
from. forms import RegistrationsForm,UpdateUserform,DepositForm
from decimal import Decimal, ROUND_DOWN

# Create your views here.
class UserCreateView(FormView):
    template_name='user/signup.html'
    form_class=RegistrationsForm
    success_url=reverse_lazy('profile')
    def form_valid(self, form):
        user=form.save()
        login(self.request,user)       
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['type']='SignUp'
        return context

class UserLoginView(LoginView):
    template_name='user/signup.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['type']='Login'
        return context
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    
class UserAcountUpdateView(View):
    template_name='user/signup.html'

    def get(self,request):
        form=UpdateUserform(instance=request.user)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=UpdateUserform(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request,self.template_name,{'form':form})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] ='User Update' 
        return context
    


class ProfileView(TemplateView):
    template_name='user/profile.html'


class DepositView(View):
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
            return redirect('profile')
        return render(request,self.template_name,{'form':form})
     
def book_borrow(request,id):
    book=Book.objects.get(pk=id)
    user_balance = request.user.account.balance
    
    print(book.book_price)
    print(book.book_quantity)
    print(request.user.account.balance)


    if book.book_quantity<1:
        messages.warning(request,'No stocks available')
        return redirect('profile')
    if user_balance>=book.book_price:
        af_balance=user_balance - book.book_price
      
        borrow=BorrowBook.objects.create(
            user=request.user,
            book_name=book.book_name,
            book_price=book.book_price,
            balance_A_B_Book=af_balance
        )
        print(borrow)
        book.book_quantity-=1
        book.save()
        # borrow.save()
        return redirect('profile')
    else:
        messages.warning(request,'Insufficient balance')
    return redirect('profile')

# def book_borrow(request,id):
#     book=Book.objects.get(pk=id)
#     book.book_quantity-=1
#     aft_balance=request.user.account.balance - book.book_price
#     if  book.car_quantity<1:
#         messages.warning(request,'The Car is out of stock')
#     else:
#         borrowed_book=BorrowBook(
#             user= request.user,
#             # car_image=car.car_image,
#             book_name=book.book_name,
#             book_price=book.car_price,
#             balance_A_B_Book=aft_balance,
#             # car_quantity=car.car_quantity,
#             # car_brand_name=car.car_brand_name
#         )
        
#         book.save()
#         borrowed_book.save()

#     return redirect('profile')   
   