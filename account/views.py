from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UserProfileForm
from django.contrib import messages
from .models import *
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
        'projects': allprojects,
        'suggested_projects': suggested_projects,  # Uncommented this line to include suggested projects
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



@login_required
def register_for_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    if project.participants.filter(id=user.id).exists():
        messages.info(request, "You have already registered for this project.",extra_tags='already')
    else:
        # Check if the maximum number of participants has been reached
        if project.max_participants and project.participants.count() >= project.max_participants:
            messages.info(request, "The maximum number of participants for this project has been reached.",extra_tags='maxparticipant')
        else:
            project.participants.add(user)
            messages.success(request, "You have successfully registered for the project.")

    return HttpResponse('project_detail')
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


