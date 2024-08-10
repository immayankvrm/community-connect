from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect(loginUser)
        else:
            form = CreateUserForm()    
    context = {'form':form}
    return render(request, 'register.html',context)


def loginUser(request):
    if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(request, username=username, password=password)
       if user is not None:
        login(request,user)
        return HttpResponse('dashboard')
       else:
        messages.info(request,'Username Or Password is incorrect') 
    context = {}
    return render(request, 'login.html',context)

def home(request):
    return render(request, 'home.html')
