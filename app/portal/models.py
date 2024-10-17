import stripe
from django.db import models
from django.contrib.auth.models import User

stripe.api_key = 'sk_test_51PxYt9KsX8iFIbQ65B3pDup2ufCUCBadwMWw5PwUN4uydWjxgyLaGkLs07HGhYe6OJosqLGAAZOuPCcjo4Bs3yKH001aaa8jRU'

class Product(models.Model):
    name = models.CharField(max_length=200)
    stripe_product_id = models.CharField(max_length=200, blank=True)
    stripe_price_id = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.stripe_product_id:
            # Create a new product in Stripe
            stripe_product = stripe.Product.create(
                name=self.name,
                description=self.description
            )
            self.stripe_product_id = stripe_product.id

            # Create a new price for the product
            stripe_price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=int(self.price * 100),  # Stripe uses cents
                currency='usd'  # Change as needed
            )
            self.stripe_price_id = stripe_price.id
        else:
            # Update existing product in Stripe
            stripe.Product.modify(
                self.stripe_product_id,
                name=self.name,
                description=self.description
            )
            # Note: Stripe doesn't allow updating prices, so we'll create a new one if price changed
            if not stripe.Price.retrieve(self.stripe_price_id).unit_amount == int(self.price * 100):
                new_price = stripe.Price.create(
                    product=self.stripe_product_id,
                    unit_amount=int(self.price * 100),
                    currency='usd'
                )
                self.stripe_price_id = new_price.id

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Archive the product in Stripe when deleted in Django
        if self.stripe_product_id:
            stripe.Product.modify(self.stripe_product_id, active=False)
        super().delete(*args, **kwargs)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} ({self.product.quantity})'