from django.urls import path
from . views import RegistrationView, LoginView, LogoutView, UserDashboardView

urlpatterns = [
    path('register/',RegistrationView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('dashboard/',UserDashboardView.as_view()),
]

#