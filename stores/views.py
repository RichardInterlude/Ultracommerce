from rest_framework import status,serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from . models import *
from . serializers import *
from django.db import transaction


# :::: CATEGORY VIEW ::::
class CategorysView(APIView):
    # create and get Categorys
    def post(self,request):
        try:
           serializers = CategorySerializers(data=request.data)
           if serializers.is_valid():
               serializers.save()
               return Response(serializers.data, status=status.HTTP_201_CREATED)
           return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self,request):
        try:
            categorys = Category.object.all()
            serializers = CategorySerializers(categorys,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CategoryView(APIView):
    def get(self,request,id):
        try:
            category = get_object_or_404(Category,id=id)
            serializers = CategorySerializers(category)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request,id):
        try:
            category = get_object_or_404(Category,id=id)
            serializers = CategorySerializers(category,data=request.data,partials= True) 
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,id):
        try:
            category = get_object_or_404(Category,id=id)
            category.delete()
            return Response({"Message":f"{category.title} deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# :::: PRODUCT VIEW ::::
class ProductsView(APIView):
    # create and get Products
    def post(self,request):
        try:
           serializers = ProductSerializers(data=request.data)
           if serializers.is_valid():
               serializers.save()
               return Response(serializers.data, status=status.HTTP_201_CREATED)
           return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self,request):
        try:
            products = Product.objects.all()
            serializers =   ProductSerializers(products,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductView(APIView):
    def get(self,request,id):
        try:
            product = get_object_or_404(Product,id=id)
            serializers = ProductSerializers(product)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request,id):
        try:
            product = get_object_or_404(Product,id=id)
            serializers = ProductSerializers(product,data=request.data,partial= True) 
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,id):
        try:
            product = get_object_or_404(Product,id=id)
            product.delete()
            return Response({"Message":f"{product.title} deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# :::: CART VIEW ::::
class AddToCart(APIView):
    def post(self,request,id):
        try:
            #  get product to add to cart
            product = get_object_or_404(Product,id=id)
            #  get cart based on session
            cart_id = request.session.get('cart_id',None)
            #  to get actual price or discounted price
            price = product.discount_price if product.discount_price else product.price


            while transaction.atomic():
                if cart_id:
                    # get the cart
                    cart = Cart.objects.filter(id=cart_id).first()
                    if cart is None:
                        cart = Cart.objects.create(total=0)
                        request.session['cart_id'] = cart.id
                    
                    # add product to cart
                    product_in_cart = cart.cartproduct_set.filter(product=product)
                    if product_in_cart.exists():
                        cartproduct = product_in_cart.last()
                        cartproduct.quantity += 1
                        cartproduct.subtotal += price
                        cartproduct.save()
                        cart.total += price
                        cart.save()
                        return Response({"Message":"item increased in cart"}, status=status.HTTP_201_CREATED)
                    else:
                        # create a new product
                        cartproduct = CartProduct.objects.create(cart=cart,product=product,quantity=1,subtotal=price)
                        cartproduct.save()
                        cart.total += price
                        cart.save()
                        return Response({"Message":"New item added successfully"}, status=status.HTTP_201_CREATED)
 
                else:
                    # to create a new cart
                    cart = Cart.objects.create(total = 0)
                    request.session['cart_id'] = cart.id
                    cartproduct = CartProduct.objects.create(cart=cart,product=product,quantity=1,subtotal=price)
                    cartproduct.save()
                    cart.total += price
                    cart.save()
                    return Response({"Message":"New item added to cart"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# :::: ACCESS CART ::::
class UserCart(APIView):
    def get(self,request):
        try:
            # check if we have cart_id or not
            cart_id = request.session.get('cart_id',None)
            if cart_id:
                # if we have cart_id we are going to grab it
                cart = get_object_or_404(Cart,id=cart_id)
                return Response({'Message':f'{Cart.total}'}, status=status.HTTP_200_OK)
            # if we dont have cart_id we just return a message
            return Response({'Message':'Cart not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Message':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# :::: MANAGE CART ::::
class ManageCart(APIView):
    def post(self,request,id):
        action = request.data.get('action')
        try:
            cart_obj = get_object_or_404(CartProduct,id=id)
            cart = cart_obj.cart
            price = cart_obj.product.discounted_price if cart_obj.product.discounted_price else cart_obj.product.price


            if action == 'inc':
                cart_obj.quantity +=1
                cart_obj.subtotal +=price
                cart_obj.save()
                cart.total +=price
                cart.save()
                return Response({'Message':'Item increased successfully'}, status=status.HTTP_200_OK)
            
            elif action == 'dcr':
                cart_obj.quantity -=1
                cart_obj.subtotal -=price
                cart_obj.save()
                cart.total -=price
                cart.save()
                return Response({'Message':'Item decreased successfully'},status=status.HTTP_200_OK)

            elif action == 'rmv':
                cart.total -=price
                cart.save()
                cart_obj.delete
                return Response({'Message':'Item removed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"Message":'Cart is yet to be found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
