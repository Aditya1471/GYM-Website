# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path
from .views import *
urlpatterns=[
    path('', logins, name="login"),
    path('index/', index,name="index"),
    path('classes/', classes, name="classes"),
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
    path('account/', Account, name="account"),
    path('signup/',signup,name="signup"),
    path('logout/', logoutuser, name="logout"),
    path('photo/', photo, name="photo"),
    path('product/', product, name="product"),
    path('product/<int:product_id>/', product_detail, name="product_detail"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart, name='cart'),
    path('cart/adjust/<int:cart_item_id>/<str:action>/', adjust_cart_item, name='adjust_cart_item'),
    # path('payment_intent/', create_payment_intent, name='create_payment_intent'),
    # path('payment/',payment,name="payment"),
    path('create-checkout-session/', create_checkout_session, name = "create-checkout-session"),
    path('success/', success, name = "success"),
    path('cancel/', cancel, name = "cancel"),
    path('customer/',customer_form, name='customer_form'),
    # path('orders/',order_list, name='order_list'),
    path('Pay/',pay_now,name='pay_now'),
    path('search/', product_query, name='product_query'),
    path('machines/', machines, name='machines'),
    path('profile/', profile, name='profile'),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('blog/', blog, name='blog'),
    path('calculator/', calculator, name='calculator'),
]
   





# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)