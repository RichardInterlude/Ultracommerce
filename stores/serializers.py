from rest_framework import serializers

from . models import *

# Category Serializer
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
       model = Category
       fields = '__all__'

# Product Serializer
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
       model = Product
       fields = '__all__'

# Cart Serializer
class CartSerializers(serializers.ModelSerializer):
    class Meta:
       model = Cart
       fields = '__all__'

# CartProduct Serializer
class CartProductSerializers(serializers.ModelSerializer):
    class Meta:
       model = CartProduct
       fields = '__all__'

# Order Serializer
class OrderSerializers(serializers.ModelSerializer):
    class Meta:
       model = Order
       fields = '__all__'

# Checkout Serializer
class CheckoutSerializers(serializers.ModelSerializer):
    class Meta:
       model = Order
       fields = '__all__'
