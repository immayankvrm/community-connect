from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Project


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'skills', 'availability', 'location', 'bio', 'user']
        # If you want to exclude the user field in the response, you can use:
        # fields = ['first_name', 'last_name', 'skills', 'availability', 'location', 'bio']


