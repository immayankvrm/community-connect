from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UserProfileForm
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import logout

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction

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
            # print('executing')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password is incorrect',extra_tags='incorrectlogin')

    context = {}
    return render(request, 'login.html', context)

def home(request):
    return render(request, 'home.html')


@login_required

def dashboard(request):
    # Filter all projects with 'In Progress' or 'Upcoming' status
    allprojects = Project.objects.filter(status__in=['In Progress', 'Upcoming'])
    
    
    # Set up pagination
    paginator = Paginator(allprojects, 3)  # Show 3 projects per page
    page = request.GET.get('page')
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        projects = paginator.page(paginator.num_pages)
    
    for project in projects:
        if project.max_participants and project.max_participants > 0:
            project.progress_percentage = (project.participants.count() / project.max_participants) * 100
        else:
            project.progress_percentage = 0

    user = request.user
    # Fetch the user profile; `get_or_create` returns a tuple (object, created)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Fetch projects the user has registered for
    userprojects = request.user.registered_projects.all()

    # Fetch projects the user is participating in
    user_participating_projects = Project.objects.filter(participants=user)

    # Filter suggested projects based on user's location and skills
    # Assuming skills are stored as comma-separated strings in both the user profile and project models
    suggested_projects = Project.objects.filter(
        location=user_profile.location,
        skills_required__icontains=user_profile.skills
    ).exclude(participants=user)
    
    # Pass the filtered projects to the template
    context = {
        'projects': projects,  # This now contains the paginated queryset
        'suggested_projects': suggested_projects,
        'userprojects': userprojects,
        'participating_projects': user_participating_projects,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def Profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        print(request.user.email)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        return render(request, 'profile_not_found.html')  # Or redirect to a suitable page

    context = {
        'user_profile': user_profile,
        'user_email': request.user.email
    }

    return render(request, 'profile_display.html', context)

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



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Project

@login_required
def register_for_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        user = request.user
        
        
        # Check if the user is already registered for the project
        if project.participants.filter(id=user.id).exists():
            return JsonResponse({'success': False, 'message': 'You are already registered for this project.'}, status=400)
        
        # Check if the project has reached max participants
        if project.max_participants and project.participants.count() >= project.max_participants:
            return JsonResponse({'success': False, 'message': 'This project is full.'}, status=400)
        
        # Register the user for the project
        project.participants.add(user)
        return JsonResponse({'success': True, 'message': 'Successfully registered for the project.'}, status=200)
    
    # If the request method is not POST, return an error
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

    #   return redirect('project_detail', project_id=project.id)



# @login_required
# def suggested_projects(request):
#     user = request.user
#     user_profile = user.userprofile  # Assuming there's a OneToOneField relationship with UserProfile
    
#     # Filter projects based on the user's skills and location
#     suggested_projects = Project.objects.filter(
#         location=user_profile.location,
#         skills_required__icontains=user_profile.skills
#     ).exclude(participants=user)

#     context = {
#         'suggested_projects': suggested_projects,
#     }

#     return render(request, 'dashboard.html', context)




def logoutUser(request):
    logout(request)  # This will log out the user
    return redirect('loginUser')  # Redirect to the login page after logout







@login_required
@transaction.atomic
def edit_profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(user, request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')

            if password_form.has_changed() and password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
            elif password_form.has_changed():
                messages.error(request, 'Please correct the error below.')

            return redirect('Profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = CreateUserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        password_form = PasswordChangeForm(user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'edit_profile.html', context)
