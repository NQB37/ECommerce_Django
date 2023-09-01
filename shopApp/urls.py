from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('items/detail/<int:pk>',views.detail, name='detail'),
    path('items/new/', views.AddItem, name='newitem'),
    path('search/', views.search, name='search'),
    path('searchresults/', views.searchresults, name='searchresults'),
    path('addtocart/<int:pk>/', views.addtocart, name='addtocart'),
    path('updatequantity/<int:pk>/', views.updatecartquantity, name='updatecartquantity'),
    path('removefromcart/<int:pk>/', views.removefromcart, name='removefromcart'),
    path('cart/', views.cart, name='cart'),
    path('clearcart/', views.clearcart, name='clearcart'),
    path('docheckout/', views.docheckout, name='docheckout'),
    path('order/', views.order, name='order'),
    path('checkout/', views.checkout, name='checkout'),
    path('customer/',views.profile, name='profile'),
    path('items/<int:pk>/delete/',views.deleteitem, name='deleteitem'),
    path('items/<int:pk>/edit/',views.edititem, name='edititem'),
    path('customers/newaddress/',views.newaddress, name='newaddress'),
    path('customers/newpayment/',views.newpayment, name='newpayment'),
    path('items/<int:pk>/review/',views.review, name='review'),
    path('adminorder/', views.adminorder, name='adminorder'),
    path('order/<int:order_id>/complete/', views.complete_order, name='complete_order'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
]