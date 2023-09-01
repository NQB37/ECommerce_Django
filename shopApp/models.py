from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='customer_images', blank=True, null=True)
    
    def __str__(self):
        return f'{self.firstname} {self.lastname}' 
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address =  models.CharField(max_length=255)
    address2 =  models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.user} {self.address} {self.state} {self.country}' 
    
class Payment(models.Model):
    PAYMENTMETHOD_CHOICES = (
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Paypal Card', 'Paypal Card'),
    )
    MONTH_CHOICES = [(str(i), str(i).zfill(2)) for i in range(1, 13)]
    YEAR_CHOICES = [(str(i), str(i)) for i in range(22, 32)]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method =  models.CharField(max_length=255, choices=PAYMENTMETHOD_CHOICES, default='Credit Card')
    name =  models.CharField(max_length=255)
    cardnumber = models.CharField(max_length=255)
    expire_month = models.CharField(max_length=2, choices=MONTH_CHOICES, default='1')
    expire_year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='23')
    cvv = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    def get_expire(self):
        return f'{self.expire_month}/{self.expire_year}'
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        
    def get_average_rating(self):
        reviews = Review.objects.filter(item=self)
        if reviews.exists():
            total_rating = sum([review.rating for review in reviews])
            return total_rating / len(reviews)
        else:
            return 0
        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
                
    def __str__(self):
        return f"Cart {self.pk} for {self.user.username}"

    def get_total_cost(self):
        total_cost = 0
        for detail in self.details.all():
            total_cost += detail.get_item_total()
        return total_cost

class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} in cart {self.cart.pk}"

    def get_item_total(self):
        return self.item.price * self.quantity
    
    def set_quantity(self, quantity):
        self.quantity = quantity
        self.save()
        
class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, default=None)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} - {self.user.username}'
    
    def get_total_cost(self):
        total_cost = 0
        for detail in self.items.all():
            total_cost += detail.get_item_total()
        return total_cost

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.item.name} ({self.quantity}) - ${self.price}'

    def get_item_total(self):
        return self.price * self.quantity
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.item}: Rating {self.rating} by {self.user}"