from django.db import models
import uuid
import secrets
from users.models import Profile

# Category
class Category(models.Model):
    title = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to='category',default="Default Title")
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.title
# Products
SIZE_CHOICES = (
    ('36-40','36-49'),
    ('41-45','41-45'),
    ('46-47','46-47'),
)
class Product(models.Model):
    title = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    price = models.BigIntegerField(null=True)
    discount_price = models.BigIntegerField(null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product',null=True)
    photo1 = models.ImageField(null=True,blank=True)
    photo2 = models.ImageField(null=True,blank=True)
    photo3 = models.ImageField(null=True,blank=True)
    brand = models.CharField(max_length=255),
    size = models.CharField(max_length=255,choices=SIZE_CHOICES,null=True)
    product_code = models.UUIDField(unique=True,default=uuid.uuid4)
    review  = models.TextField( null=True)
    rating = models.BigIntegerField(default=0)
    is_available  = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.title   
    
    def save(self, *args, **kwargs):
        if not self.product_code:
            self.product_code = uuid.uuid4
        super().save(*args,**kwargs)
# Cart
class Cart(models.Model):
    total = models.BigIntegerField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return f'cart {self.id} - total{self.total}'

# Cart Products
class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.BigIntegerField()
    subtotal = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return f'Cart Product -- {self.cart.id} - {self.quantity}'

# Order
ORDER_STATUS =(
    ('PENDING','PENDING'),
    ('APPROVED','APPROVED'),
    ('DELIVERED','DELIVERED'),
    ('CANCELLED','CANCELLED')
)

PAYMENT_METHOD = (
    ('Paystack','Paystack'),
    ('Paypal','Paypal'),
    ('Bank Transfer','Bank Transfer'),
    ('Stripe','Stripe')
)
class Order(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    order_by = models.CharField(max_length=255)
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    amount = models.PositiveBigIntegerField()
    subtotal = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD,default='PAYSTACK')
    ref = models.CharField(max_length=255,null=True,blank=True,unique=True)

    def __str__(self):
        pass

    def save(self,*args,**kwargs):
        ref = secrets.token_urlsafe(50)
        objects_with_the_same_ref =Order.objects.filter(ref=ref)
        if not objects_with_the_same_ref:
            self.ref = ref
        super().save(*args,**kwargs)
    def amount_value(self)->int:
        return self.amount * 100
# Payment
