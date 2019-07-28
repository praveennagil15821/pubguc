from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser,Profile
from service.models import Category

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)
        

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields= ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pay_image','daily_limit','offer']        
        labels = {'pay_image':'PayTM QR Code',
                'daily_limit':'Orders Daily limit',
                'offer':'Offers'
                }

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title','price']        
