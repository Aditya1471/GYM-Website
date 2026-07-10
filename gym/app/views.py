from django.shortcuts import render, HttpResponse, redirect,get_object_or_404,reverse
from .models import *
from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.contrib import messages
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
import stripe
from .forms import CustomerForm
# import json
# Set your secret key


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,"index.html" )   

def classes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,"classes.html")

def contact(request):
    if not request.user.is_authenticated:
      return redirect('login')
    if request.method== 'POST':
        name= request.POST.get('name')
        email= request.POST.get('email')
        sub= request.POST.get('sub')
        message= request.POST.get('message')
        print(name,email,sub,message)
        user= Contact(name=name, email=email, sub=sub, message=message)
        user.save()
        
    return render(request,"contact.html")

def about(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,"about.html")

def logins(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
         return render(request,'login.html')
    
    
def signup(request):
    frm= UserCreationForm()
    if request.method=='POST':
        frm= UserCreationForm(request.POST)
        if frm.is_valid():
            frm.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    return render(request,"signup.html", {'fm': frm})

def Account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    frm= UserCreationForm()
    if request.method=='POST': 
        frm = UserCreationForm(request.POST) 
        if frm.is_valid(): 
            frm.save() 
            return redirect('account')
    return render(request, 'account.html', {'fm':frm})    

def logoutuser(request):
    logout(request)
    return redirect('login')
    

def photo(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'photo.html')



def product_detail(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    """View to display the details of a single product."""
    product = get_object_or_404(Product, id=product_id)
    category = product.category
    similar_products = category.products.exclude(id=product_id)
    return render(request, 'product_detail.html', {'product': product,'category': category,'similar_products': similar_products})

def product(request):
    if not request.user.is_authenticated:
        return redirect('login')
    """View to display all products along with categories."""
    categories = Category.objects.all()
    products = Product.objects.all()  # Fetch all products to display
    return render(request, 'product.html', {'categories': categories, 'products': products})

def product_query(request):
    if not request.user.is_authenticated:
        return redirect('login')
    query = request.GET.get('q', '')
    if query:
        categories = Category.objects.filter(products__name__icontains=query).distinct()
    else:
        categories = Category.objects.all()
    return render(request, 'product.html', {'categories': categories, 'query': query})

def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.products.all()  # Get CartItems related to the current Cart
    total_price = sum(cart_item.quantity * cart_item.product.price for cart_item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'cart': cart})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{product.name} Added in your cart.")
    return redirect('product')




def add_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    qty = request.GET.get('qty')
    if qty:
        try:
            qty_val = int(qty)
            if qty_val > 0:
                if created:
                    cart_item.quantity = qty_val
                else:
                    cart_item.quantity += qty_val
            else:
                cart_item.quantity += 1
        except ValueError:
            cart_item.quantity += 1
    else:
        cart_item.quantity += 1
        
    cart_item.save()
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} removed from your cart.")
    return redirect('cart')

def adjust_cart_item(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    product_name = cart_item.product.name

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1

    cart_item.save()
    return redirect('cart')

# views.py


# @csrf_exempt
# def create_payment_intent(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             amount = int(data.get('amount', 0))
#             currency = data.get('currency', 'usd')
#             payment_method_id = data.get('payment_method_id')

#             if not payment_method_id:
#                 return JsonResponse({'error': 'Payment method ID is required'}, status=400)

#             intent = stripe.PaymentIntent.create(
#                 amount=amount,  # Amount in cents
#                 currency=currency,
#                 payment_method=payment_method_id,
#                 confirmation_method='manual',
#                 confirm=True,
#             )
#             return JsonResponse({'client_secret': intent.client_secret})
#         except stripe.error.CardError as e:
#             return JsonResponse({'error': str(e)}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)
# def payment(request):
#     return render(request, 'payment.html')
def customer_form(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Retrieve existing delivery details if already saved
    customer_instance = Customer.objects.filter(user=request.user).last()

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer_instance)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  
            customer.save()
            return redirect('pay_now')  
    else:
        form = CustomerForm(instance=customer_instance)
    return render(request, 'customer_form.html', {'form': form})

def pay_now(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        pass
    return render(request, 'list.html')



import logging
from django.conf import settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)  
    total_price = 0

    for cart_item in cart_items:
        unit_price_in_paise = int(cart_item.product.price * 100)
        item_total_amount = unit_price_in_paise * cart_item.quantity
        total_price += item_total_amount
    print(f"Total price of the cart: {total_price} paise")
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': total_price, 
                        'product_data': {
                            'name': "Cart Total",  
                        },
                    },
                    'quantity': 1, 
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(checkout_session.url, code=303)
        except stripe.error.StripeError as e:
            return HttpResponseBadRequest(f"Error creating checkout session: {str(e)}")
    else:
        return HttpResponseBadRequest("Invalid request method.")
def success(request):
    return render(request, 'checkout.html', {"payment_status": "success_url"})

def cancel(request):
    return render(request, 'cancel.html', {"payment_status": "cancel_url"})



def example_function(**kwargs):
  try:
    stripe.PaymentIntent.create(**kwargs)
  except stripe.error.CardError as e:
    logging.error("A payment error occurred: {}".format(e.user_message))
  except stripe.error.InvalidRequestError:
    logging.error("An invalid request occurred.")
  except Exception:
    logging.error("Another problem occurred, maybe unrelated to Stripe.")
  else:
    logging.info("No error.")

def machines(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'machines.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'profile.html', {'addresses': addresses})

def admin_panel(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('index')
    
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    recent_customers = Customer.objects.all().order_by('-id')[:5]
    recent_products = Product.objects.all().order_by('-id')[:5]
    estimated_mrr = total_users * 1499
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_customers': total_customers,
        'recent_users': recent_users,
        'recent_customers': recent_customers,
        'recent_products': recent_products,
        'estimated_mrr': estimated_mrr,
    }
    return render(request, 'admin_panel.html', context)

def blog(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'blog.html')

def calculator(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'calculator.html')