from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # Removing password-based authentication
        if 'usable_password' in self.fields:
            del self.fields['usable_password']





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'skills', 'availability', 'location', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
