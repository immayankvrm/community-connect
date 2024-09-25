from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginUser, name='loginUser'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create_profile/', create_profile, name='create_profile'),
    path('my_profile/', Profile, name='Profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('logout/', logoutUser, name='logoutUser'),
    path('register_for_project/<int:project_id>/', register_for_project, name='register_for_project'),

]