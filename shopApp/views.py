from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Item, Cart, CartDetail, OrderDetail, Order, Review, Customer, Address, Payment
from .forms import SignupForm, AddItemForm, ItemSearch, EditItemForm, AddressForm, PaymentForm, ReviewForm
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:99]
    category = Category.objects.all()
    
    return render(request, "index.html",{
        'category': category,
        'items': items,
    })

def contact(request):
    return render(request, "contact.html")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create a User instance but don't save it yet
            user.save()  # Save the User instance

            # Create a Customer instance and associate it with the User
            customer = Customer.objects.create(
                user=user,
                firstname=form.cleaned_data['firstname'],
                lastname=form.cleaned_data['lastname'],
                # Add more fields as needed
            )
            return redirect('/login/')
    else:
        form = SignupForm()
        
    return render(request, 'signup.html',{
        'form': form
    })
    
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    reviews = Review.objects.filter(item=item).exclude(pk=pk)[0:99]
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:99]
    
    
    return render(request, 'detail.html', {
        'item': item,
        'related_items': related_items,
        'reviews' : reviews,
    })
    
def search(request):
    return render(request, 'search.html')

def searchresults(request):
    query = request.GET.get('query')
    results = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'searchresults.html', context)
    
def AddItem(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('detail', pk=item.id)
    form = AddItemForm()
    return render(request, 'newitem.html', {
        'title': 'New Item', 
        'form': form
        })

def edititem(request,pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'edititem.html', {
        'form': form
        })

def deleteitem(request, pk):
    item = get_object_or_404(Item, pk=pk)
    reviews = Review.objects.filter(item=item)

    items = Item.objects.filter(is_sold=False)[0:99]
    category = Category.objects.all()
    
    # Delete the item and its reviews
    item.delete()
    reviews.delete()

    return render(request,'index.html',{
        'category': category,
        'items': items,
    })    

@require_POST
def addtocart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        try:
            cart_detail = CartDetail.objects.get(cart=cart, item=item)
            cart_detail.quantity += 1
            cart_detail.save()
        except CartDetail.DoesNotExist:
            cart_detail = CartDetail(cart=cart, item=item, quantity=1)
            cart_detail.save()
    return redirect('detail', pk=item.id)

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cartdetail = CartDetail.objects.filter(cart=cart)
        carttotal = cart.get_total_cost()
    except Cart.DoesNotExist:
        cartdetail = None
        carttotal = 0
    
    return render(request, 'cart.html', {
        'cartdetail': cartdetail,
        'carttotal': carttotal,
        })
    
@require_POST
def updatecartquantity(request, pk):
    item = CartDetail.objects.get(pk = pk)
    quantity = int(request.POST['quantity'])
    item.set_quantity(quantity)
    item.save()
    
    return redirect('cart')

@require_POST
def removefromcart(request, pk):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_detail = CartDetail.objects.get(pk=pk)
        cart_detail.delete()
    except Cart.DoesNotExist or CartDetail.DoesNotExist:
        return redirect('cart')
    return redirect('cart')

@require_POST
def clearcart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart.delete()
    except Cart.DoesNotExist or CartDetail.DoesNotExist:
        return redirect('cart')
    return redirect('cart')


@require_POST
def docheckout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_details = CartDetail.objects.filter(cart=cart)
    
    selected_address_id = request.POST.get('selected-address')
    selected_payment_id = request.POST.get('selected-payment')

    selected_address = get_object_or_404(Address, id=selected_address_id)
    selected_payment = get_object_or_404(Payment, id=selected_payment_id)
    
    order = Order.objects.create(
        user=request.user,
        address=selected_address,
        payment=selected_payment
        )
    
    for cart_detail in cart_details:
        OrderDetail.objects.create(
            order=order,
            item=cart_detail.item,
            quantity=cart_detail.quantity,
            price=cart_detail.item.price,
        )
    cart.delete()
    
    return render(request,'checkoutsuccess.html')
    
def order(request):
    user_orders = Order.objects.filter(user=request.user)
    pending_orders = user_orders.filter(status='PENDING')
    completed_orders = user_orders.filter(status='COMPLETED')
    cancelled_orders = user_orders.filter(status='CANCELLED')
    return render(request, 'order.html', {
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders
    })
    
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        carttotal = cart.get_total_cost()
        addresses = Address.objects.filter(user=request.user)
        payments = Payment.objects.filter(user=request.user)
    except Cart.DoesNotExist:
        carttotal = 0
    
    return render(request, 'checkout.html',{
        'carttotal': carttotal,
        'addresses': addresses, 
        'payments': payments
    })

def profile(request):
    customer = Customer.objects.get(user=request.user)
    addresses = Address.objects.filter(user = request.user)
    payments = Payment.objects.filter(user = request.user)
    return render(request, 'profile.html',{
        'customer': customer,
        'addresses' : addresses,
        'payments' : payments
    })

def newaddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, request.FILES)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')
    form = AddressForm()
    return render(request, 'address.html', {
        'form': form
        })

def newpayment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            return redirect('profile')
    form = PaymentForm()
    return render(request, 'payment.html', {
        'form': form
        })
    
def review(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.item = item
            review.save()
            return redirect('detail',pk)
        else:
            return ReviewForm()
        
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def adminorder(request):
    user_orders = Order.objects.all()
    pending_orders = user_orders.filter(status='PENDING')
    return render(request, 'adminorder.html', {
        'pending_orders': pending_orders,
    })
    
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'COMPLETED'
    order.save()
    return redirect('adminorder')  

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'CANCELLED'
    order.save()
    return redirect('adminorder') 