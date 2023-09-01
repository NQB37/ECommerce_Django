from django.contrib import admin
from .models import Category, Item, Cart, CartDetail, Order, OrderDetail, Customer,Review, Address, Payment

        
# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartDetail)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Address)
admin.site.register(Payment)