import stripe
from .models import UserPayment
from django.conf import settings
from watch.models import Product
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.db.models import Sum



# @login_required(login_url="login")
# def product_page(request, product_id):
#     stripe.api_key = settings.STRIPE_SECRET_KEY_TEST

#     try:
#         product = Product.objects.get(id=product_id)

#     except Product.DoesNotExist:
#         raise Http404("Product does not exist")

#     if request.method == "POST":
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "unit_amount": int(product.price * 100),
#                         "product_data": {
#                             "name": product.name,
#                             "description": product.description,
#                         },
#                     },
#                     "quantity": 1,
#                 },
#             ],
#             mode="payment",
#             customer_creation="always",
#             success_url=settings.REDIRECT_DOMAIN
#             + f"/payment_successful?session_id={{CHECKOUT_SESSION_ID}}&product_id={product.id}",
#             cancel_url=settings.REDIRECT_DOMAIN + "/payment_cancelled",
#         )
#         return redirect(checkout_session.url, code=303)

#     return render(request, "checkout.html", {"product": product})


# @login_required(login_url="login")
# def product_page(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY_TEST

#     # try:
#     #     product = Product.objects.get(id=product_id)

#     # except Product.DoesNotExist:
#     #     raise Http404("Product does not exist")

#     if request.method == "POST":
#         price=request.POST["total"]
#         print(price)
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "unit_amount": int(price)*100,
                      
#                     },
#                     "quantity": 1,
#                 },
#             ],
#             mode="payment",
#             customer_creation="always",
#             # success_url=settings.REDIRECT_DOMAIN
#             # + f"/payment_successful?session_id={{CHECKOUT_SESSION_ID}}&product_id={product.id}",
#             # cancel_url=settings.REDIRECT_DOMAIN + "/payment_cancelled",
#             success_url="https://www.google.com/",
#             cancel_url="https://www.youtube.com/"
#         )
#         return redirect(checkout_session.url)

#     return render(request, "product_page.html")
#     # return render(request, "product_page.html", {"product": product})


@login_required(login_url="login")
def product_page(request,product_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
        
    if request.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(product.price * 100),
                        "product_data": {
                            "name": product.product_name,
                            "description": product.desc,
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="http://127.0.0.1:8000/",
            cancel_url="https://www.youtube.com/",
        )
        return redirect(checkout_session.url)

    return render(request, "checkout.html", {"product": product})
@login_required
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_payment = UserPayment(
        user=request.user, checkout_id=checkout_session_id, is_successful=True
    )
    
        # Clear the cart after successful payment
    cart = Cart.objects.get(user=request.user)
    cart.products.clear()  # Remove all associated products from the cart

    user_payment.save()

    payment_history = UserPayment.objects.filter(user=request.user)
    print(payment_history)
    return render(
        request,
        "payment_successful.html",
        {"customer": customer, "payment_history": payment_history},
    )


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, "payment_cancelled.html")


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    payload = request.body
    signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id", None)
        user_payment = UserPayment.objects.get(checkout_id=session_id)
        user_payment.is_successful = True
        user_payment.save()
    return HttpResponse(status=200)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect('payment:cart')

# @login_required
# def cart(request):
#     cart = Cart.objects.get(user=request.user)
#     products = cart.products.all()
#     return render(request, 'cart.html', {'products': products})

@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    products = cart.products.all()
    total_price = products.aggregate(sum_price=Sum('price')).get('sum_price', 0)
    context = {
        'products': products,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)