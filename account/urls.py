from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginUser, name='loginUser'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create_profile/', create_profile, name='create_profile'),

]