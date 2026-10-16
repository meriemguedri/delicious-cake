from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model  = CustomUser
        fields = ('username', 'email', 'profile_picture')

class CustomUserEditForm(UserChangeForm):
    password = None  # Passwortfeld verstecken
    class Meta:
        model  = CustomUser
        fields = ('username', 'email', 'profile_picture')