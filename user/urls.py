from django.urls import path
from.views import UserCreateView,UserLoginView,UserLogoutView,UserAcountUpdateView,ProfileView,DepositView,book_borrow

urlpatterns = [
    path("signup/",UserCreateView.as_view(),name='signup'),
    path("login/",UserLoginView.as_view(),name='login'),
    path("logout/",UserLogoutView.as_view(),name='logout'),
    path("update/",UserAcountUpdateView.as_view(),name='update'),
    path("profile/",ProfileView.as_view(),name='profile'),
    path("deposit/",DepositView.as_view(),name='deposit'),
    path("borrow/<int:id>/",book_borrow,name='borrow'),
]
