from django.urls import path
from .views import loginUser,register,home

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginUser, name='loginUser'),
    path('register/', register, name='register'),
]