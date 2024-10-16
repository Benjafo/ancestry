from django.urls import path
from . import views

app_name = 'portal'
urlpatterns = [
    path('products/', views.products, name='products'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe-webhook'),
    # path('checkout/<int:product_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
]