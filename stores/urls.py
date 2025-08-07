from django.urls import path
from . views import *
urlpatterns = [
    path('categorys/',CategorysView.as_view()),
    path('category/<str:id>/',CategoryView.as_view()),
    path('products/',ProductsView.as_view()),
    path('product/<str:id>/',ProductView.as_view()),
    path('addtocart/<str:id>/',AddToCart.as_view()),
    path('usercart/',UserCart.as_view()),
    path('managecart/<str:id>/',ManageCart.as_view()),
    ]
