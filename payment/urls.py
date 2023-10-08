from django.urls import path
from .views import (
    # CheckoutView,
    payment_cancelled,
    payment_successful,
    # PaymentHistoryView,
    product_page,
    stripe_webhook,
    add_to_cart,
    cart,
        
    

)
app_name = "payment"


urlpatterns = [
    # path("checkout/<int:product_id>/", CheckoutView.as_view(), name="checkout"),
    # path("checkout/<int:product_id>/", product_page, name="checkout"),
    path("product_page/", product_page, name="product_page"),
    path("payment_successful/", payment_successful, name="payment_successful"),
    path("payment_cancelled/", payment_cancelled, name="payment_cancelled"),
    path("stripe_webhook/   ", stripe_webhook, name="stripe_webhook"),
    # path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    # path('cart/', cart, name='cart'),
    path("checkout/<int:product_id>",product_page,name='checkout')


    # path("payment_history/", PaymentHistoryView.as_view(), name="payment_history"),
    # path("payment_history/<int:userid>", purchasedHistory, name="payment_history"),
    # path("createcheckout-session",CheckoutSessionView.as_view(),name="create-checkout-session"),
]
