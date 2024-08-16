from django.db import models
from django.contrib.auth.forms import UserCreationForm
# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    skills = models.CharField(max_length=300)
    availability = models.BooleanField(default=True)
    location = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)  # Additional field for biography
    #profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=50, choices=[
        ('Upcoming', 'Upcoming'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ])
    category = models.CharField(max_length=50)
    
    participants = models.ManyToManyField(User, related_name='registered_projects', blank=True)
    
    skills_required = models.CharField(max_length=255, blank=True, null=True)
    max_participants = models.IntegerField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    
    

    def __str__(self):
        return self.name
