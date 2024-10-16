import stripe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import CartItem, Product

import logging
logger = logging.getLogger(__name__)

stripe.api_key = 'sk_test_51PxYt9KsX8iFIbQ65B3pDup2ufCUCBadwMWw5PwUN4uydWjxgyLaGkLs07HGhYe6OJosqLGAAZOuPCcjo4Bs3yKH001aaa8jRU'
STRIPE_WEBHOOK_SECRET = 'whsec_dbc2b6ec690566118c74565e321047c05e153787ced7cb5ff67b6c46c002fb24'
DOMAIN = 'http://localhost:8000/api/portal'

# def create_checkout_session(request, product_id, quantity=1):
#     product = get_object_or_404(Product, pk=product_id)
#     try:
#         checkout_session = stripe.checkout.Session.create(
#             line_items = [
#                 {
#                     'price': product.stripe_price_id,
#                     'quantity': quantity
#                 }
#             ],
#             mode='payment',
#             success_url=f'{DOMAIN}/success.html',
#             cancel_url=f'{DOMAIN}/cancel.html'
#         )
#     except Exception as e:
#         return HttpResponse(str(e), status=400)
#     return redirect(checkout_session.url, 303)

def products(request):
    products = stripe.Product.list()
    context = { 'products': products }
    return render(request, 'portal/products.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    return render(request, 'cart.html', {'cart_items': cart_items})

#####################################################################################3
## Handle stripe webhooks
#####################################################################################3
@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'product.created':
        handle_product_created(event.data.object)
    elif event.type == 'product.updated':
        handle_product_updated(event.data.object)
    elif event.type == 'product.deleted':
        handle_product_deleted(event.data.object)
    elif event.type == 'price.created':
        handle_price_created(event.data.object)
    elif event.type == 'price.updated':
        handle_price_updated(event.data.object)
    elif event.type == 'price.deleted':
        handle_price_deleted(event.data.object)

    return HttpResponse(status=200)

def handle_product_created(stripe_product):
    logger.info(f"Creating product: {stripe_product.id}")
    try:
        Product.objects.create(
            name=stripe_product.name,
            stripe_product_id=stripe_product.id,
            description=stripe_product.description
        )
        logger.info(f"Product created successfully: {stripe_product.id}")
    except Exception as e:
        logger.error(f"Error creating product {stripe_product.id}: {str(e)}")

def handle_product_updated(stripe_product):
    product = Product.objects.filter(stripe_product_id=stripe_product.id).first()
    if product:
        product.name = stripe_product.name
        product.description = stripe_product.description
        product.save()

def handle_product_deleted(stripe_product):
    Product.objects.filter(stripe_product_id=stripe_product.id).delete()

def handle_price_created(stripe_price):
    product = Product.objects.filter(stripe_product_id=stripe_price.product).first()
    if product:
        product.stripe_price_id = stripe_price.id
        product.price = stripe_price.unit_amount / 100  # Convert cents to dollars
        product.save()

def handle_price_updated(stripe_price):
    product = Product.objects.filter(stripe_price_id=stripe_price.id).first()
    if product:
        product.price = stripe_price.unit_amount / 100
        product.save()

def handle_price_deleted(stripe_price):
    product = Product.objects.filter(stripe_price_id=stripe_price.id).first()
    if product:
        product.stripe_price_id = ''
        product.save()