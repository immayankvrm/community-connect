from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UserProfileForm
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import authenticate,login
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required


def register(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect('loginUser')
    
    context = {'form': form}
    return render(request, 'register.html', context)



def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Check if the user has a filled profile
            try:
                profile = user.userprofile
                # Redirect to profile creation page if not filled
                if not profile.first_name or not profile.last_name:
                    return redirect('create_profile')
            except UserProfile.DoesNotExist:
                # Redirect to profile creation page if profile doesn't exist
                return redirect('create_profile')

        # Redirect to dashboard if profile exists and is filled
            print('executing')
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'login.html', context)

def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def create_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        return redirect('dashboard')  # Redirect if the profile already exists
    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('dashboard')  # Redirect to dashboard after profile creation
        else:
            form = UserProfileForm()

        context = {'form': form}
        return render(request, 'profile_form.html', context)
