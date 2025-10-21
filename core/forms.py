from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "profile_image", "bio")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("image", "caption")
